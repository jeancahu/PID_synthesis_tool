from django.urls import path

from . import views

urlpatterns = [
    path('', views.identify_plant, name='pidtuningtool'),
    path('model_as_input', views.identify_plant, name='pidtuningtool_mi'),
    path('response_as_input', views.identify_plant, name='pidtuningtool_ri'),
]
