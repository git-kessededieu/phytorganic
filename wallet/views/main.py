# Create your views here.
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView, TemplateView
from werkzeug.security import check_password_hash

from backend.models import Member
from wallet import MODULE
from wallet.forms import AddBalanceForm
from wallet.models import MainWallet, MainWalletTransactions
from wallet.transactions import operation_tnx


class MainDepositView(LoginRequiredMixin, CreateView):
    model = MainWallet
    form_class = AddBalanceForm
    template_name = 'backend/wallet/main/main-deposit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "main_deposit"
        context['page_title'] = _("Main Deposit")
        context['page_info'] = _("Main Deposit")
        context['member'] = Member.objects.get(user = self.request.user)
        context['balance'] = MainWallet.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        post = request.POST
        if post:
            balance = post.get("balance", "")
            if int(balance) == 0:
                messages.warning(request, "{} can't be added to the main balance".format(int(balance)))
                return redirect('wallet:main-deposit')
            else:
                wallet_balance = MainWallet.objects.first()
                if wallet_balance is None:
                    wallet = MainWallet(balance = balance)
                    wallet.save()
                else:
                    wallet_balance.balance = F('balance') + balance
                    wallet_balance.save()

                messages.success(request, "Your balance was successfully updated!")
                return redirect('wallet:main-deposit')
        else:
            messages.error(request, "An error occurred!")
            return redirect('wallet:main-deposit')


class MainTransferView(LoginRequiredMixin, TemplateView):
    template_name = 'backend/wallet/main/main_transfer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "main_transfer"
        context['page_title'] = _("Phytorganic to Member Transfer")
        context['page_info'] = _("Phytorganic to Member Transfer")
        context['member'] = Member.objects.get(user = self.request.user)
        context['balance'] = MainWallet.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        post = request.POST
        pass
        amount = post.get("amount", 0)
        t_receiver = post.get("username", "")
        security_code = post.get('security_code', "")
        member = self.request.user.member
        system_balance = MainWallet.objects.first()

        try:
            receiver = Member.objects.get(username = t_receiver)
            wallet = "wallet1"
        except Member.DoesNotExist:
            messages.warning(request, _("Receiver doesn't exist !"))
            return redirect('wallet:main-transfer')

        check = check_password_hash(member.security_code, security_code)
        if check:
            if system_balance.balance >= Decimal(amount):

                operation_data = {
                    'member': member,
                    'wallet': wallet,
                    'receiver': receiver,
                    'operation': 'transfer',
                    'created_by': member
                }
                transaction_status = operation_tnx("M2m", Decimal(amount), **operation_data)
                if transaction_status:
                    messages.success(request, _("Green Gold transfer done successfully !"))
                else:
                    messages.error(request, _("An error occurred !!!"))
            else:
                messages.error(request, _("Main balance is not sufficient to process this transfer !!!"))
        else:
            messages.error(request, _("Security Password incorrect, please try again."))

        return redirect('wallet:main-transfer')


class MainTransactionView(LoginRequiredMixin, ListView):
    model = MainWalletTransactions
    template_name = 'backend/wallet/main/main_transactions.html'
    paginate_by = 20
    context_object_name = 'tnx_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "main_transactions"
        context['page_title'] = _("Main Transactions")
        context['page_info'] = _("Main Transactions")
        context['member'] = Member.objects.get(user = self.request.user)
        context['balance'] = MainWallet.objects.first()
        return context
