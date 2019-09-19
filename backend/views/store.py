from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import ListView
from werkzeug.security import check_password_hash

from backend import MODULE
from backend.bonus import maintenance_incentive_handler
from backend.forms import MaintenancePackForm
from backend.models import MaintenancePack
from backend.transactions import order_tnx_handler
from wallet.models import MemberWallet


class MaintenancePackView(LoginRequiredMixin, ListView):
    model = MaintenancePack
    template_name = 'backend/store/maintenance.html'
    form_class = MaintenancePackForm
    context_object_name = "pack_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "maintenance"
        context['page_title'] = _("Maintenance Packs")
        context['page_info'] = _("Maintenance Packs")
        context['member'] = self.request.user.member
        return context

    def post(self, request):
        post = request.POST
        print(post)
        security_code = post.get('security_code', None)
        pack_id = post.get('pack_id', None)
        member = self.request.user.member
        print(member)
        print(pack_id)
        check = check_password_hash(member.security_code, security_code)
        if check:
            pack = MaintenancePack.objects.get(id = pack_id)
            print(pack)
            member_wallet = MemberWallet.objects.get(member = member).wallet2
            if member_wallet >= pack.price:
                maintenance_incentive_handler(request, pack.id)

                order_tnx_handler(member = member, order_type = "MP", pack = pack, payment_mode = "wallet2",
                                  delivery_method = "self")

                messages.success(request, _("Maintenance Pack Ordered successfully !"))
            else:
                messages.error(request, _("Your Wallet balance is not sufficient to complete this order !!!"))
        else:
            messages.error(request, _("Wallet Password incorrect, please try again."))

        print(check)
