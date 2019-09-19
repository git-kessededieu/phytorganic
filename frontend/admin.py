from django.apps import apps
from django.contrib import admin

from frontend.models import *

for model in apps.get_app_config('frontend').models.values():
    admin.site.register(model)

# for model in apps.get_app_config('backend').models.values():
#     admin.site.register(model)


class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class FAQCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class FAQAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('question',)}
    search_fields = ['question']


admin.site.unregister(ProductCategory)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
admin.site.unregister(FAQCategory)
admin.site.register(FAQCategory, FAQCategoryAdmin)
admin.site.unregister(FAQ)
admin.site.register(FAQ, FAQAdmin)
