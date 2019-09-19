from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, UpdateView, DetailView

from backend import MODULE
from backend.forms import MemberForm, BankInfoForm
from backend.models import Member, BankInfo, MemberCounter
from frontend.forms import MigrationForm


class DashboardMenuView(LoginRequiredMixin, TemplateView):
    template_name = 'backend/partials/header.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = MigrationForm()
        context = {
            'page_name': self.kwargs['page_name'],
            'form': form
        }

        return TemplateResponse(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = MigrationForm(request.POST)
        if form.is_valid():
            migration = form.save()
            migration.save()

            context = {
                'status': 'success'
            }
            response = self.get(request, context)
            return response


class DashboardView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'backend/home.html'

    def get_object(self, queryset = None):
        return self.request.user.member

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "dashboard"
        context['page_title'] = _("Dashboard")
        context['page_info'] = _("Dashboard")
        context['member_counters'] = MemberCounter.objects.filter(member = self.get_object())
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Member
    template_name = 'backend/user/profile.html'
    form_class = MemberForm

    def get_object(self, queryset = None):
        return self.request.user.member

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "profile"
        context['page_title'] = _("Profile")
        context['page_info'] = _("Member Information")
        return context


class BankInfoView(LoginRequiredMixin, UpdateView):
    model = BankInfo
    template_name = 'backend/user/bank_info.html'
    form_class = BankInfoForm
    obj = None

    def get_object(self, queryset = None):
        return self.request.user.member

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "bank_info"
        context['page_title'] = _("Bank Info")
        context['page_info'] = _("Bank Info")
        return context
