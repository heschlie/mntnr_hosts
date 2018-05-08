from django.contrib import admin
from django.apps import apps

from mntnr_hosts import models


for model in apps.get_app_config('mntnr_hosts').get_models():
    if model != models.Host:
        admin.site.register(model)