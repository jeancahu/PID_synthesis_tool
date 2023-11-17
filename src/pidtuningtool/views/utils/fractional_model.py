from pidtune.models import plant
from pidtuningtool.models import Plant as db_plant

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.core.exceptions import ObjectDoesNotExist

import re

@require_POST
def plant_model_fractional(request, data):
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

    return JsonResponse(status=200, data={
        "message": "Web push successful",
        "url_slug": tmp_plant.url_ref,
        "simulation": plant_model.toResponse(),
        'model_id': "fractional",
    })

@require_POST
def plant_open_loop_response_fractional(request, data):
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
                              "simulation": plant_model.toResponse(),
                              'model_id': model_id,
                              })
