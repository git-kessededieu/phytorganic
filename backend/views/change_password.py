from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import TemplateView
from werkzeug.security import generate_password_hash

from backend import MODULE
from backend.models import Member


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'backend/user/change_password.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        context = {
            'page_name': "change_password",
            'form': form,
            'module': MODULE,
            'page_title': _("Password Change"),
            'page_info': _("Password Change")
        }

        return TemplateResponse(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('backend:change-password')
        else:
            messages.error(request, 'An error occurred')
            context = {
                'status': 'error'
            }
            self.get(request, context)
            return redirect('backend:change-password')


class ChangeSecurityPasswordView(LoginRequiredMixin, TemplateView):
    model = Member
    template_name = 'backend/user/change_security_password.html'

    def get(self, request, *args, **kwargs):
        context = {
            'page_name': "change_security_password",
            'module': MODULE,
            'page_title': _("Security Password Change"),
            'page_info': _("Security Password Change")
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        member = self.request.user.member
        # password = request.POST.get("password", None)
        new_password = request.POST.get("new_password", None)
        cf_password = request.POST.get("cf_password", None)

        if member and new_password == cf_password:
            member.security_code = generate_password_hash(new_password)
            member.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('backend:change-security-password')

        else:
            messages.error(request, 'Password confirmation don\'t match !')
            return redirect('backend:change-security-password')
