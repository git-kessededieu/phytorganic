"""phytorganic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.utils.translation import ugettext_lazy

from backend.views import member
from frontend.views import HomeView

admin.site.site_title = ugettext_lazy('Administration PHYTORGANIC')
admin.site.site_header = ugettext_lazy('Administration PHYTORGANIC')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('dashboard/', include('backend.urls')),
    path('wallet/', include('wallet.urls')),
    path('<str:username>', HomeView.as_view()),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += [
    path('get_member/<str:username>', member.get_member, name = 'get_member'),
    re_path(r'^validate_username/$', member.validate_username, name = 'validate_username'),
    re_path(r'^validate_sponsor/$', member.validate_sponsor, name = 'validate_sponsor'),
    re_path(r'^validate_email/$', member.validate_email, name = 'validate_email'),
    re_path(r'^validate_placement_name/$', member.validate_placement_name, name = 'validate_placement_name'),
    re_path(r'^validate_placement_mode/$', member.validate_placement_mode, name = 'validate_placement_mode'),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG is True:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
