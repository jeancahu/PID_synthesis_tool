from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from pidtuningtool.__version__ import __version__ as se_version # TODO

from pidtune.models import plant, system as c_sys
from pidtuningtool.models import Plant as db_plant

import json
import re

from .utils.fractional_model import plant_model_fractional, plant_open_loop_response_fractional

## Util functions
def valid_response_input(strg, search=re.compile(r'^[0-9\n\r\tEe+-.]+$').search):
    """
    Test if the response syntaxis is valid
    """
    return bool(search(strg))

## Views
@require_GET
def identify_plant(request):
    """
    Index/landing page containing a card for each identification method implemented
    """
    context = {
        'model_id': 'undefined',
    }
    return render(request, 'pidtuningtool/landing.html', context)

@require_GET
def plant_step_response_input(request, model_id="fractional"):
    """
    Input file in {TXT,TSV,CSV} format to be identified
    """
    context = {
        'model_id': model_id,
    }
    return render(request, 'pidtuningtool/plant_step_response_input.html', context)

@require_GET
def model_input(request, model_id='fractional'):
    context = {
        'model_id': model_id,
    }
    return render(request, 'pidtuningtool/model_as_input.html', context)

@require_GET
def pidtune_results(request, data_input, plant_slug):
    tmp_plant = get_object_or_404(db_plant, url_ref=plant_slug)
    plant_model = plant.FractionalOrderModel(
            alpha=float(tmp_plant.plant_params['alpha'],),
            time_constant=float(tmp_plant.plant_params['T']),
            proportional_constant=float(tmp_plant.plant_params['K']),
            dead_time_constant=float(tmp_plant.plant_params['L'])
    )
    controllers = plant_model.controllers
    controller_params = []

    for l_ctl in controllers:

        l_sys = c_sys.ClosedLoop(
            controller = l_ctl,
            plant = plant_model
        )

        ## Get the closed loop simulation for the system: controller -> plant
        t_vect, y_vect, y_vect_reg, servo_iae, regulatory_iae = l_sys.step_response(
            servo_magnitude=1, disturbance_magnitude=0.5)
        controller_params.append(
            l_ctl.toDict()
        )
        controller_params[-1].update({
            'y_vect': y_vect,
            'y_vect_reg': y_vect_reg,
            't_vect': t_vect,
            'IAE': servo_iae,
            'IAE_reg': regulatory_iae
        })

    context = {
        'model_id': model_id,
        "v_param": tmp_plant.plant_params['alpha'],
        "T_param": tmp_plant.plant_params['T'],
        "K_param": tmp_plant.plant_params['K'],
        "L_param": tmp_plant.plant_params['L'],
        "model_IAE": tmp_plant.plant_params['IAE'],
        "controller_params": controller_params,
        "from_model": data_input == "model",
    }
    return render(request, 'pidtuningtool/results_page.html', context)

@require_GET
def pidtune_results_alfaro(request):#, data_input, plant_slug):
    #tmp_plant = get_object_or_404(db_plant, url_ref=plant_slug)
    plant_model = plant.FractionalOrderModel(
            alpha=float(1),
            time_constant=float(1),
            proportional_constant=float(1),
            dead_time_constant=float(1)
    )
    controllers = plant_model.controllers
    controller_params = []

    for l_ctl in controllers:

        l_sys = c_sys.ClosedLoop(
            controller = l_ctl,
            plant = plant_model
        )

        ## Get the closed loop simulation for the system: controller -> plant
        #t_vect, y_vect, y_vect_reg, servo_iae, regulatory_iae = l_sys.step_response(
        #    servo_magnitude=1, disturbance_magnitude=0.5)
        controller_params.append(
            l_ctl.toDict()
        )
        '''controller_params[-1].update({
            'y_vect': y_vect,
            'y_vect_reg': y_vect_reg,
            't_vect': t_vect,
            'IAE': servo_iae,
            'IAE_reg': regulatory_iae
        })
    '''
    context = {
        #'model_id': model_id,
        "v_param": 45,
        "T_param": 32,
        "K_param": 32,
        "L_param": 32,
        "model_IAE": 42,
        "controller_params": controller_params,
        "from_model": True,
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

        if 'textcontent' not in data or not 'model_id' in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        model_id = data['model_id']
        print(model_id)
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

        if model_id == 'fractional':
            return plant_open_loop_response_fractional(request, data)
        # elif model_id == 'alfaro123c_etc':
        #     return plant_model_fractional(request, data)

        # elif model_id == 'alfaro123c_etcetc':
        #     return plant_model_fractional(request, data)

        else:
            return JsonResponse(status=400, data={"message": "Invalid model ID"})

    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})

@require_POST
def plant_model(request):
    # Plant fractional order model previously calculated by the user
    try:
        data = request.POST
        if not request.session or not request.session.session_key:
            # expiry 15 minutes
            request.session.set_expiry(900)
            request.session.save()

        if 'model_id' not in data:
            return JsonResponse(status=400, data={"message": "No model ID"})

        if data['model_id'] == 'fractional':
            return plant_model_fractional(request, data)

        # elif data['model_id'] == 'alfaro123c_etc':
        #     return plant_model_fractional(request, data)

        # elif data['model_id'] == 'alfaro123c_etcetc':
        #     return plant_model_fractional(request, data)

        else:
            return JsonResponse(status=400, data={"message": "Invalid model ID"})

    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
