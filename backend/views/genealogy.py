from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import ListView

from backend import MODULE
from backend.models import Member
from frontend.enums import PLACEMENT_MODE, MAX_GENERATION_NUMBER


class SponsorGenealogyView(LoginRequiredMixin, ListView):
    model = Member
    template_name = 'backend/genealogy/sponsor_genealogy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "sponsor_genealogy"
        context['page_title'] = _("Sponsor Genealogy")
        context['page_info'] = _("Sponsor Genealogy")
        context['members'] = self.request.user.member.get_descendants(include_self = True)
        return context


class PlacementGenealogyView(LoginRequiredMixin, ListView):
    model = Member
    member = None
    is_member = True
    template_name = 'backend/genealogy/placement_genealogy.html'

    def get_queryset(self):
        if "username" in self.kwargs:
            try:
                self.member = Member.objects.get(username = self.kwargs["username"])
                self.is_member = False
            except Member.DoesNotExist:
                self.member = self.request.user.member
        else:
            self.member = self.request.user.member

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "placement_genealogy"
        context['page_title'] = _("Placement Genealogy")
        context['page_info'] = _("Placement Genealogy")
        level = self.member.get_level() + MAX_GENERATION_NUMBER
        members = self.member.get_descendants(include_self = True).filter(
            level__gte = self.member.get_level()).filter(level__lt = level).order_by("placement_mode")
        context['descendants'] = [
            {
                'username': member.username,
                'grade': member.get_grade_display(),
                'status': member.status,
                'bv_left': member.member_bv.left,
                'bv_right': member.member_bv.right,
                'placement_name': member.placement_name,
                'full_name': member.full_name,
                'get_descendant_count': member.get_descendant_count(),
                'members_left': member.get_descendants().filter(placement_mode = 'left').count(),
                'members_right': member.get_descendants().filter(placement_mode = 'right').count()
            } for member in members
        ]
        context['is_root'] = self.member == self.member.get_root()
        context['member'] = self.member
        context['is_member'] = self.is_member
        return context


class DirectDownLineView(LoginRequiredMixin, ListView):
    model = Member
    context_object_name = "downline"
    template_name = 'backend/genealogy/direct_downline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "direct_downline"
        context['page_title'] = _("Direct Downline")
        context['page_info'] = _("Direct Downline")
        member = self.request.user.member
        sponsorship = Member.objects.filter(sponsor = member.username)
        context['left_side'] = sponsorship.filter(placement_mode = PLACEMENT_MODE.left)
        context['right_side'] = sponsorship.filter(placement_mode = PLACEMENT_MODE.right)
        return context
