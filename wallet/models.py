from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from backend.models import Member, OperationType
from frontend.enums import OPERATION
from frontend.enums import PAYMENT_MODE, OPERATION_TYPE


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username = 'deleted')[0]


class MainWallet(models.Model):
    balance = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0, verbose_name = "Balance",
                                  help_text = "Balance")

    class Meta:
        db_table = 'main_wallet'
        verbose_name = 'Main Wallet'
        verbose_name_plural = 'Main Wallets'

    @staticmethod
    def get_absolute_url():
        return reverse('wallet:deposit')

    def __str__(self):
        return "Main Wallet {}".format(self.balance)


class MemberWallet(models.Model):
    member = models.OneToOneField(Member, models.CASCADE, related_name = "member_wallet", verbose_name = "Wallet Owner")
    wallet1 = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0, verbose_name = "Green Wallet 1",
                                  help_text = "Income (For Bonus)")
    wallet2 = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0, verbose_name = "Green Wallet 2",
                                  help_text = "Outcome")

    class Meta:
        db_table = 'member_wallet'
        verbose_name = 'Member Wallet'
        verbose_name_plural = 'Members Wallets'

    def __str__(self):
        return "{0} : {1} - {2}".format(self.member, self.wallet1, self.wallet2)


class MainWalletTransactions(models.Model):
    id = models.BigAutoField(primary_key = True)
    sender = models.ForeignKey(Member, on_delete = models.SET_NULL, blank = True, null = True,
                               related_name = "main_wallet_sender", editable = False)
    receiver = models.ForeignKey(Member, on_delete = models.SET_NULL, blank = True, null = True,
                                 related_name = "main_wallet_receiver", editable = False)
    operation = models.CharField(max_length = 60, choices = OPERATION, editable = False, verbose_name = "Operation")
    type = models.CharField(max_length = 60, choices = OPERATION_TYPE, editable = False, verbose_name = _("Type"))
    amount = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0, editable = False)
    origin = models.ForeignKey(OperationType, on_delete = models.SET_NULL, blank = True, null = True, editable = False,
                               verbose_name = _("Origin"))
    created_by = models.ForeignKey(Member, on_delete = models.SET_DEFAULT, default = 1,
                                   related_name = 'main_wallet_tnx_created_by', editable = False)
    tnx_date = models.DateTimeField(auto_now_add = True, editable = False)

    class Meta:
        db_table = 'main_wallet_tnx'
        verbose_name = 'Main Wallet Transaction'
        verbose_name_plural = 'Main Wallets Transactions'


class MemberWalletTransactions(models.Model):
    id = models.BigAutoField(primary_key = True)
    sender = models.ForeignKey(Member, on_delete = models.SET_NULL, blank = True, null = True,
                               related_name = "member_wallet_sender", editable = False)
    receiver = models.ForeignKey(Member, on_delete = models.SET_NULL, blank = True, null = True,
                                 related_name = "member_wallet_receiver", editable = False)
    wallet = models.CharField(max_length = 15, choices = PAYMENT_MODE, editable = False,
                              verbose_name = _("Payment Mode"))
    operation = models.CharField(max_length = 60, choices = OPERATION, editable = False, verbose_name = _("Operation"))
    type = models.CharField(max_length = 60, choices = OPERATION_TYPE, editable = False, verbose_name = _("Type"))
    amount = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0, editable = False)
    origin = models.ForeignKey(OperationType, on_delete = models.SET_NULL, blank = True, null = True, editable = False,
                               verbose_name = _("Origin"))
    created_by = models.ForeignKey(Member, on_delete = models.SET_DEFAULT, default = 1,
                                   related_name = 'member_wallet_tnx_created_by', editable = False)
    tnx_date = models.DateTimeField(auto_now_add = True, editable = False)

    class Meta:
        db_table = 'member_wallet_tnx'
        verbose_name = 'Member Wallet Transaction'
        verbose_name_plural = 'Members Wallets Transactions'
