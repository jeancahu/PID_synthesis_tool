from django.shortcuts import render
# from django.contrib.auth.decorators import login_required # TODO
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .__version__ import __version__ as se_version # TODO

# from django.conf import settings # TODO

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
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data:
            if 'step' not in data['body'] or 'plant' not in data['body'] or 'time' not in data['body']:
                return JsonResponse(status=400, data={"message": "Invalid data format"})

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})

@require_POST
def plant_fractional_model(request):
    # Plant fractional order model previously calculated by the user
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data:
            if 'v' not in data['body'] or \
               'T' not in data['body'] or \
               'K' not in data['body'] or \
               'L' not in data['body']:
                return JsonResponse(status=400, data={"message": "Invalid data format"})

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
