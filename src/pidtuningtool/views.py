from django.shortcuts import render
# from django.contrib.auth.decorators import login_required # TODO
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .__version__ import __version__ as se_version # TODO

from pidtune.models import plant

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


@require_POST
def plant_open_loop_response(request):
    # Open loop plant response when a step signal is applied
    try:
        data = request.POST

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

        print(str(plant_model))
        for controller in plant_model.tune_controllers():
            print(controller)

        return JsonResponse(status=200, data={"message": "Web push successful", "simulation": plant_model.toResponse()})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})

@require_POST
def plant_fractional_model(request):
    # Plant fractional order model previously calculated by the user
    try:
        data = request.POST

        if 'in_frac' not in data or \
           'in_time' not in data or \
           'in_prop' not in data or \
           'in_dtime' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        plant_model = plant.FractionalOrderModel(
            alpha=float(data["in_frac"]),
            time_constant=float(data["in_time"]),
            proportional_constant=float(data["in_prop"]),
            dead_time_constant=float(data["in_dtime"])
        )

        print(str(plant_model))
        for controller in plant_model.tune_controllers():
            print(controller)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
