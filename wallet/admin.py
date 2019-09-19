from django.apps import apps
from django.contrib import admin

from wallet.models import *

for model in apps.get_app_config('wallet').models.values():
    admin.site.register(model)
