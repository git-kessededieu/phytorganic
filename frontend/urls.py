from django.urls import path, re_path

from .views import *

app_name = 'frontend'

urlpatterns = [
    path('frontend/menu/<str:page_name>', FrontMenuView.as_view(), name = 'front-menu'),
    path('member-migration', MigrationView.as_view(), name = "member-migration"),
    path('landing', WelcomeView.as_view(), name = ""),
    path('', HomeView.as_view(), name = "home"),
    path('about', AboutView.as_view(), name = "about"),
    path('products', ProductListView.as_view(), name = "products"),
    path('products/<str:slug>', ProductDetailsView.as_view(), name = "product"),
    path('faq', FAQView.as_view(), name = "faq"),
    path('about', AboutView.as_view(), name = "about"),

    re_path(r'^ajax/validate_username/$', views.validate_username, name = 'validate_username'),
    re_path(r'^ajax/validate_sponsor/$', views.validate_sponsor, name = 'validate_sponsor'),
    re_path(r'^ajax/validate_email/$', views.validate_email, name = 'validate_email'),
    re_path(r'^ajax/validate_placement_name/$', views.validate_placement_name, name = 'validate_placement_name'),
    re_path(r'^ajax/validate_placement_mode/$', views.validate_placement_mode, name = 'validate_placement_mode'),
]
