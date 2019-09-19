from django.apps import apps
from django.contrib import admin

from backend.models import *

for model in apps.get_app_config('backend').models.values():
    admin.site.register(model)


class MemberAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = (
    'username', 'full_name', 'sponsor', 'parent', 'placement_name', 'placement_mode', 'leadership', 'status',
    'created_at',)


admin.site.unregister(Member)
admin.site.register(Member, MemberAdmin)
