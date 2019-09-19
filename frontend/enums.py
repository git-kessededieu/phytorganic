from django.utils.translation import gettext as _
from model_utils import Choices

PLACEMENT_MODE = Choices(('left', _('Left')), ('right', _('Right')))

GRADES = Choices(('silver', _('Silver')), ('gold', _('Gold')), ('diamond', _('Diamond')))

GENDER = Choices(('male', _('Male')), ('female', _('Female')))

STATUS = Choices((-1, _('Draft')), (0, _('Unpublished')), (1, _('Published')))

COUNTRIES = Choices(("CI", _('Côte d\'Ivoire')))

PAYMENT_MODE = Choices(("wallet1", _('Green Wallet 1')), ("wallet2", _('Green Wallet 2')))

DELIVERY = Choices(('self', _('Self Collect')), ('courier', _('Courier')))

OPERATION = Choices(('activation', _('Activation')), ('registration', _('Registration')), ('upgrade', _('Upgrade')),
                    ('bonus', _('Bonus')))

OPERATION_TYPE = Choices(('credit', _('Credit')), ('debit', _('Debit')))

BV_SIDE = Choices(('left', _('Left')), ('right', _('Right')))

SPONSORSHIP_BONUS = {
    "SILVER_TO_SILVER": 40,
    "SILVER_TO_GOLD": 30,
    "SILVER_TO_DIAMOND": 20,
}

UPGRADE_DAYS = {
    "SILVER_GOLD": 60,
    "GOLD_DIAMOND": 30
}

SPONSORSHIP_MATRIX = [[40, 30, 20], [40, 40, 30], [40, 40, 40]]

ACTIVATION_AMOUNT = 100

ACTIVATION_BV = 25

_ACTIVATION_MATRIX = [[1, 40], [2, 10], [3, 10], [4, 5], [5, 5], [6, 3], [7, 2], [8, 2], [9, 2], [10, 2]]
ACTIVATION_MATRIX = [40, 10, 10, 5, 5, 3, 2, 2, 2, 2]

TEEPS_PERCENT = 5

MEMBER_TO_MEMBER = "m2m"
MEMBER_TO_MAIN = "m2M"
MAIN_TO_MEMBER = "M2m"

PROCESSES = [MEMBER_TO_MEMBER, MEMBER_TO_MAIN, MAIN_TO_MEMBER]

CREDIT_WALLET = "wallet1"
DEBIT_WALLET = "wallet2"

MAX_GENERATION_NUMBER = 4

MAINTENANCE_PARING_PERCENT = 10
