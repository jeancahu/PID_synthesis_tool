from django.db import models
from autoslug.fields import AutoSlugField
from random import sample
import string

# Create your models here.

def default_empty_json(): # TODO
    return {}

def default_random_slug(instance):
    return instance[:2] + ''.join(sample(string.digits, 3)) + \
        instance[2:4] + ''.join(sample(string.digits, 5)) + \
        instance[4:6] + ''.join(sample(string.digits, 3))

class Plant(models.Model):
    tuner_user = models.CharField(max_length=200, default = "anonymous", help_text = "Session Key", unique=True)
    url_ref = AutoSlugField(populate_from='tuner_user', slugify=default_random_slug, unique=True)
    plant_creation =  models.DateTimeField(
        # Time and date the history was upload
        auto_now_add = True,
        editable = False,
        blank = False
    )

    plant_params = models.JSONField(
        default = default_empty_json,
        blank = False,
        editable = False
    )

    class Meta:
        verbose_name = "Plant"
        verbose_name_plural = "Plants"

    def __str__(self):
        return '{} - ({})'.format(
            self.pk,
            self.plant_creation.strftime("%Y-%m-%d")
        )

