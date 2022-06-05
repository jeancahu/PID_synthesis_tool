from django.urls import path

from . import views

urlpatterns = [
    path('', views.identify_plant, name='pidtuningtool'),
    path('model_as_input', views.fractional_order_model_input, name='pidtuningtool_mi'),
    path('response_as_input', views.plant_step_response_input, name='pidtuningtool_ri'), # TODO multiple responses

    path('plant_fractional_model', views.plant_fractional_model, name='pidtuningtool_post_mi'),
    path('plant_open_loop_response', views.plant_open_loop_response, name='pidtuningtool_post_ri'),
]
