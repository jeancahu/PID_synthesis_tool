from django.urls import path

from . import views

urlpatterns = [
    path('', views.identify_plant, name='pidtuningtool'),
    path('model_as_input', views.fractional_order_model_input, name='pidtuningtool_mi'),
    path('response_as_input', views.plant_step_response_input, name='pidtuningtool_ri'), # TODO multiple responses
]
