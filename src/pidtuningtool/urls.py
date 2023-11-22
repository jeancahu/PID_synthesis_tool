from django.urls import path, re_path

from .views import main

urlpatterns = [
    path('', main.identify_plant, name='pidtuningtool'),
    path('model_as_input/<str:model_id>', main.model_input, name='pidtuningtool_mi'),
    path('response_as_input/<str:model_id>', main.plant_step_response_input, name='pidtuningtool_ri'),

    re_path('results_from_(?P<data_input>\w{5,8})_(?P<plant_slug>\w{16,18})', main.pidtune_results, name='pidtuningtool_results'),
    path('results_from_alfaro', main.pidtune_results_alfaro, name='pidtuningtool_results_alfaro'), 

    path('plant_model', main.plant_model, name='pidtuningtool_post_mi'),
    path('plant_open_loop_response', main.plant_open_loop_response, name='pidtuningtool_post_ri'),
]
