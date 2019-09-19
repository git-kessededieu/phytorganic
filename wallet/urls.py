from django.urls import path

from wallet.views import *

app_name = 'wallet'

urlpatterns = [
    path('member-transfer', MemberTransferView.as_view(), name = "member-transfer"),
    path('member-transactions/<str:wallet>', MemberTransactionView.as_view(), name = "member-transactions"),

    path('main-deposit', MainDepositView.as_view(), name = "main-deposit"),
    path('main-transfer', MainTransferView.as_view(), name = "main-transfer"),
    path('main-transactions', MainTransactionView.as_view(), name = "main-transactions"),
]
