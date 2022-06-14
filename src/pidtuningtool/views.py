from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required # TODO
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .__version__ import __version__ as se_version # TODO

from pidtune.models import plant, system as c_sys
from .models import Plant as db_plant

import json
import re
## Util functions
def valid_response_input(strg, search=re.compile(r'^[0-9\n\r\tEe+-.]+$').search):
    return bool(search(strg))

## Views
@require_GET
def identify_plant(request):
    context = {
    }
    return render(request, 'pidtuningtool/identify_input.html', context)

@require_GET
def fractional_order_model_input(request):
    context = {
    }
    return render(request, 'pidtuningtool/fractional_order_model_input.html', context)

@require_GET
def plant_step_response_input(request):
    context = {
    }
    return render(request, 'pidtuningtool/plant_step_response_input.html', context)

@require_GET
def pidtune_results(request, data_input, plant_slug):
    tmp_plant = get_object_or_404(db_plant, url_ref=plant_slug)
    plant_model = plant.FractionalOrderModel(
            alpha=float(tmp_plant.plant_params['alpha'],),
            time_constant=float(tmp_plant.plant_params['T']),
            proportional_constant=float(tmp_plant.plant_params['K']),
            dead_time_constant=float(tmp_plant.plant_params['L'])
    )
    controllers = plant_model.tune_controllers()
    controller_params = []

    for l_ctl in controllers:

        l_sys = c_sys.ClosedLoop(
            controller = l_ctl,
            plant = plant_model
        )

        t_vect, y_vect = l_sys.step_response()
        controller_params.append(
            l_ctl.toDict()
        )
        controller_params[-1].update({
                'y_vect': y_vect,
                't_vect': t_vect
        })

    context = {
        "v_param": tmp_plant.plant_params['alpha'],
        "T_param": tmp_plant.plant_params['T'],
        "K_param": tmp_plant.plant_params['K'],
        "L_param": tmp_plant.plant_params['L'],
        "model_IAE": tmp_plant.plant_params['IAE'],
        "controller_params": controller_params,
        "from_model": data_input == "model",
    }
    return render(request, 'pidtuningtool/results_page.html', context)


@require_POST
def plant_open_loop_response(request):
    # Open loop plant response when a step signal is applied
    try:
        data = request.POST
        if not request.session or not request.session.session_key:
            # expiry 15 minutes
            request.session.set_expiry(900)
            request.session.save()

        if 'textcontent' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        data = data["textcontent"];

        if len(data) == 0:
            return JsonResponse(status=400, data={"message": "Invalid data no lenght"})

        data = re.sub(r'[;, ]', '\t', data, flags=re.MULTILINE)
        data = data.replace('\r', '')

        if not valid_response_input(data):
            # If format is not valid drop first line and try again
            data = "\n".join(data.split("/n")[1:])
            if not valid_response_input(data):
                return JsonResponse(status=400, data={"message": "Invalid data bad syntax"})

        time_vector=[]
        step_vector=[]
        resp_vector=[]

        try:
            for row in data.split('\n'):
                # Drop ghost rows
                if not len(row):
                    continue

                row = re.sub(r'\t{1,}', '\t', row) ## Removes null columns
                row = re.sub(r'^\t', '', row) ## Removes begin fake column

                # Append columns its respective vector
                col1,col2,col3 = row.split("\t")
                time_vector.append(float(col1))
                step_vector.append(float(col2))
                resp_vector.append(float(col3))

        except ValueError as e:
            return JsonResponse(status=400, data={"message": "Invalid data, corrupt rows: {}".format(e)})

        ## Plant processing
        try:
            plant_model = plant.FractionalOrderModel(
                time_vector=time_vector,
                step_vector=step_vector,
                resp_vector=resp_vector
            )
        except ValueError as e:
            return JsonResponse(status=400, data={"message": "Invalid data, {}".format(e)})

        try: # Save the plant params in database
            tmp_plant = db_plant.objects.get(tuner_user=request.session.session_key)
            tmp_plant.plant_params = plant_model.toDict()
        except ObjectDoesNotExist:
            tmp_plant = db_plant(
                tuner_user = request.session.session_key,
                plant_params = plant_model.toDict()
            )
        tmp_plant.save()

        return JsonResponse(status=200,
                            data={"message": "Web push successful",
                                  "url_slug": tmp_plant.url_ref,
                                  "simulation": plant_model.toResponse()})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})

@require_POST
def plant_fractional_model(request):
    # Plant fractional order model previously calculated by the user
    try:
        data = request.POST
        if not request.session or not request.session.session_key:
            # expiry 15 minutes
            request.session.set_expiry(900)
            request.session.save()

        if 'in_frac' not in data or \
           'in_time' not in data or \
           'in_prop' not in data or \
           'in_dtime' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        try:
            plant_model = plant.FractionalOrderModel(
                alpha=float(data["in_frac"]),
                time_constant=float(data["in_time"]),
                proportional_constant=float(data["in_prop"]),
                dead_time_constant=float(data["in_dtime"])
            )
        except ValueError as e:
            err_msg = "Invalid input: {}".format(e)
            err_msg = re.sub(r'[()\']', '', err_msg)
            err_msg = re.sub(r', , , ', ' - ', err_msg)
            err_msg = re.sub(r',', '', err_msg)

            return JsonResponse(status=400, data={"message": err_msg})

        try: # Save the plant params in database
            tmp_plant = db_plant.objects.get(tuner_user=request.session.session_key)
            tmp_plant.plant_params = plant_model.toDict()
        except ObjectDoesNotExist:
            tmp_plant = db_plant(
                tuner_user = request.session.session_key,
                plant_params = plant_model.toDict()
            )
        tmp_plant.save()

        return JsonResponse(status=200, data={"message": "Web push successful", "url_slug": tmp_plant.url_ref})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
