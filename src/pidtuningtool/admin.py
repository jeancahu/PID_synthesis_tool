from django.contrib import admin
from .models import Plant

# Register your models here.
@admin.register(Plant)
class ADMINPlant(admin.ModelAdmin):
    readonly_fields = ['tuner_user', 'url_ref', 'plant_params']
