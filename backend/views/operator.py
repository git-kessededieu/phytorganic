from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, CreateView
from werkzeug.security import check_password_hash

from backend.forms import MemberForm, OrderInfoForm
from backend.models import Member, Pack
from backend.operations import member_registration, member_activation
from frontend.enums import ACTIVATION_AMOUNT
from wallet.forms import MemberWalletForm
from wallet.models import MemberWallet

MODULE = "genealogy"


class ActivationView(LoginRequiredMixin, TemplateView):
    template_name = 'backend/operator/activation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "activation"
        context['page_title'] = _("Activation")
        context['page_info'] = _("Activation")
        context['member'] = self.request.user.member
        return context

    def post(self, request, *args, **kwargs):
        post = request.POST
        print(post)

        security_code = post.get('security_code', None)

        sender = self.request.user.member
        receiver_username = post.get('username', None)
        amount = post.get('amount', ACTIVATION_AMOUNT)

        try:
            receiver = Member.objects.get(username = receiver_username)
        except Member.DoesNotExist:
            messages.warning(request, _("Member doesn't exist !"))
            return redirect('backend:activation')

        check = check_password_hash(sender.security_code, security_code)
        if check:
            if sender.member_wallet.wallet2 >= amount:
                activation_data = {
                    'sender': sender,
                    'receiver': receiver,
                    'amount': Decimal(amount)
                }
                activated = member_activation(request, data = activation_data)
                print("Activated => {}".format(activated))
                if activated is True:
                    messages.success(request, _("Member activated successfully !"))
                else:
                    messages.error(request, _("An error occurred !"))
            else:
                messages.error(request, _("Your Wallet balance is not sufficient to complete this activation !!!"))
        else:
            messages.error(request, _("Security Password incorrect, please try again."))

        return redirect('backend:activation')


class RegisterView(LoginRequiredMixin, CreateView):
    model = Member
    template_name = 'backend/operator/registration.html'
    form_class = MemberForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = MODULE
        context['page_name'] = "register"
        context['page_title'] = _("Register")
        context['page_info'] = _("Register")
        context['order_form'] = OrderInfoForm
        context['wallet_form'] = MemberWalletForm
        context['packs'] = Pack.objects.all()
        context['wallet'] = MemberWallet.objects.filter(member = self.request.user.member).first()

        return context

    def post(self, request, *args, **kwargs):
        post = request.POST
        print(post)

        registered = member_registration(request, data = post)
        print("Registered => {}".format(registered))
        if registered is True:
            messages.success(request, 'Member registered successfully !')
        else:
            messages.error(request, 'An error occurred, Member registration failed !')
        return redirect('backend:register')
