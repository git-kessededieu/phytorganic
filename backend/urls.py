from django.urls import path, re_path

from backend.views import member
from .views import *

app_name = 'backend'

urlpatterns = [
    path('menu/<str:page_name>', DashboardMenuView.as_view(), name = 'dashboard-menu'),
    path('', DashboardView.as_view(), name = "home"),
    path('profile', ProfileView.as_view(), name = "profile"),
    path('bank-info', BankInfoView.as_view(), name = "bank-info"),
    path('sponsor-genealogy', SponsorGenealogyView.as_view(), name = "sponsor-genealogy"),
    path('placement-genealogy', PlacementGenealogyView.as_view(), name = "placement-genealogy"),
    path('placement-genealogy/<str:username>', PlacementGenealogyView.as_view(), name = "member-placement-genealogy"),
    path('direct-downline', DirectDownLineView.as_view(), name = "direct-downline"),
    path('register', RegisterView.as_view(), name = "register"),
    path('upgrade', RegisterView.as_view(), name = "upgrade"),
    path('activation', ActivationView.as_view(), name = "activation"),
    path('maintenance', MaintenancePackView.as_view(), name = "maintenance"),
]

urlpatterns += [
    # re_path(r'^ajax/get_member/$', get_member, name = 'get_member'),
    # re_path(r'^ajax/get_member_activation/$', get_member_activation, name = 'get_member_activation'),
]

urlpatterns += [
    path('change-password/', ChangePasswordView.as_view(), name = 'change-password'),
    path('change-security-password/', ChangeSecurityPasswordView.as_view(), name = 'change-security-password'),
]

urlpatterns += [
    re_path(r'^backend/validate_username/$', member.validate_username, name = 'validate_username'),
    re_path(r'^backend/validate_sponsor/$', member.validate_sponsor, name = 'validate_sponsor'),
    re_path(r'^backend/validate_email/$', member.validate_email, name = 'validate_email'),
    re_path(r'^backend/validate_placement_name/$', member.validate_placement_name, name = 'validate_placement_name'),
    re_path(r'^backend/validate_placement_mode/$', member.validate_placement_mode, name = 'validate_placement_mode'),
]

urlpatterns += [
    re_path(r'^register/get_sponsor/$', views.validate_sponsor, name = 'get_sponsor'),
    re_path(r'^register/get_placement_name/$', views.get_placement_name, name = 'get_placement_name'),
    re_path(r'^register/validate_placement_mode/$', views.validate_placement_mode, name = 'validate_placement_mode'),
    re_path(r'^register/validate_username/$', views.validate_username, name = 'validate_username'),
    re_path(r'^register/validate_email/$', views.validate_email, name = 'validate_email'),
    re_path(r'^register/check_security_code/$', views.check_security_code, name = 'check_security_code'),
    re_path(r'^register/check_balance/$', views.check_balance, name = 'check_balance'),
]
