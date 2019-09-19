# Create your views here.
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView, TemplateView
from werkzeug.security import check_password_hash

from backend.models import Member
from frontend.enums import PAYMENT_MODE
from wallet import MODULE
from wallet.models import MemberWalletTransactions
from wallet.transactions import operation_tnx


class MemberTransferView(LoginRequiredMixin, TemplateView):
    template_name = 'backend/wallet/member/member_transfer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "member_transfer"
        context['page_title'] = _("Member Wallet Transfer")
        context['page_info'] = _("Member Wallet Transfer")
        context['member'] = Member.objects.get(user = self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        post = request.POST
        pass
        amount = post.get("amount", 0)
        t_receiver = post.get("username", "")
        security_code = post.get('security_code', "")
        member = self.request.user.member

        try:
            if len(t_receiver) == 0:
                receiver = member
                wallet = "wallet1"
            else:
                receiver = Member.objects.get(username = t_receiver)
                wallet = "wallet2"
        except Member.DoesNotExist:
            messages.warning(request, _("Receiver doesn't exist !"))
            return redirect('wallet:member-transfer')

        check = check_password_hash(member.security_code, security_code)
        if check:
            if receiver == member:
                cond = member.member_wallet.wallet1 >= Decimal(amount)
            else:
                cond = member.member_wallet.wallet2 >= Decimal(amount)

            if cond:
                operation_data = {
                    'member': member,
                    'wallet': wallet,
                    'sender': member,
                    'receiver': receiver,
                    'operation': 'transfer',
                    'created_by': member
                }
                transaction_status = operation_tnx("m2m", Decimal(amount), **operation_data)
                if transaction_status:
                    messages.success(request, _("Green Gold transfer done successfully !"))
                else:
                    messages.error(request, _("An error occurred !!!"))
            else:
                messages.error(request, _("Your Wallet balance is not sufficient to process this transfer !!!"))
        else:
            messages.error(request, _("Wallet Password incorrect, please try again."))

        return redirect('wallet:member-transfer')


class MemberTransactionView(LoginRequiredMixin, ListView):
    template_name = 'backend/wallet/member/member_transactions.html'
    paginate_by = 10
    context_object_name = 'tnx_list'

    def get_queryset(self):
        member = self.request.user.member
        return MemberWalletTransactions.objects.filter(Q(sender = member) | Q(receiver = member),
                                                       wallet = self.kwargs.get('wallet')).order_by('-tnx_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        wallet = self.kwargs.get('wallet')
        context['page_name'] = "{}_transactions".format(wallet)
        context['page_title'] = _("{} Transactions".format(PAYMENT_MODE.__getitem__(wallet)))
        context['page_info'] = _("{} Transactions".format(PAYMENT_MODE.__getitem__(wallet)))
        context['member'] = self.request.user.member
        context['wallet'] = wallet
        return context
