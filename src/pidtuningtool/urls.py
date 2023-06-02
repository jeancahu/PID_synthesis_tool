from django.urls import path, re_path

from .views import main

urlpatterns = [
    path('', main.identify_plant, name='pidtuningtool'),
    path('frac_model_as_input', main.fractional_order_model_input, name='pidtuningtool_mi'),
    path('frac_model_response_as_input', main.plant_step_response_input, name='pidtuningtool_ri'), # TODO multiple responses
    re_path('results_from_(?P<data_input>\w{5,8})_(?P<plant_slug>\w{16,18})', main.pidtune_results, name='pidtuningtool_results'),

    path('plant_fractional_model', main.plant_fractional_model, name='pidtuningtool_post_mi'),
    path('plant_open_loop_response', main.plant_open_loop_response, name='pidtuningtool_post_ri'),
]
