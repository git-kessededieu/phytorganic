from backend import logger
from backend.methods import ancestors_bv_update
from backend.models import Member, MaintenancePack, OperationType
from frontend.enums import TEEPS_PERCENT, SPONSORSHIP_MATRIX, ACTIVATION_MATRIX, ACTIVATION_BV
from wallet.transactions import operation_tnx


def teeps_handler(request, **kwargs):
    """THE ENROLLER RECEIVES THE MATCHING PERCENTAGE GRADE"""
    pack = kwargs.get("pack", None)
    teep = pack.bv * TEEPS_PERCENT / 100

    enroller = request.user.member

    operation_data = {
        'member': enroller,
        'wallet': "wallet1",
        'sender': None,
        'receiver': None,
        'operation': 'teeps',
        'created_by': enroller
    }
    return operation_tnx("M2m", teep, **operation_data)


def activation_bonus_handler(request, **kwargs):
    """THE SPONSOR RECEIVES THE MATCHING PERCENTAGE GRADE"""
    member = kwargs.get("member", None)
    operation = kwargs.get("operation", None)
    a_m = ACTIVATION_MATRIX
    created_by = member
    origin = OperationType.objects.filter(code_name = operation).first()

    """UPDATE SPONSOR BV"""
    ancestors_bv_update(member, ACTIVATION_BV, origin)

    """WALLET INCOME"""
    try:
        ancestors = member.get_ancestors(ascending = True)
        ancestors = [ancestor for ancestor in ancestors if ancestor.status]
    except ValueError as e:
        logger.error(e)
        ancestors = []
    # print("Ancestors => {}".format(ancestors))

    operation_data = {
        'wallet': "wallet1",
        'sender': member,
        'operation': origin,
        'created_by': created_by
    }

    for ancestor, value in zip(ancestors, a_m):
        if ancestor:
            print("Ancestor => {}, Value => {}".format(ancestor, value))
            bonus_amount = ACTIVATION_BV * value / 100
            operation_data['member'] = ancestor
            operation_data['receiver'] = ancestor
            operation_tnx("M2m", bonus_amount, **operation_data)


def sponsorship_bonus_handler(request, **kwargs):
    """THE SPONSOR RECEIVES THE MATCHING PERCENTAGE GRADE"""
    sponsor = kwargs.get("sponsor", None)
    pack = kwargs.get("pack", None)
    s_m = SPONSORSHIP_MATRIX
    created_by = request.user.member

    sponsor_info = Member.objects.get(username__exact = sponsor)

    bonus_amount = 0

    """WALLET INCOME"""
    if sponsor_info.grade == "silver":
        bonus_amount = pack.bv * s_m[0][pack.level] / 100
    if sponsor_info.grade == "gold":
        bonus_amount = pack.bv * s_m[1][pack.level] / 100
    if sponsor_info.grade == "diamond":
        bonus_amount = pack.bv * s_m[2][pack.level] / 100

    operation_data = {
        'member': sponsor_info,
        'wallet': "wallet1",
        'sender': None,
        'receiver': sponsor_info,
        'operation': 'sponsorship_bonus',
        'created_by': created_by
    }
    return operation_tnx("M2m", bonus_amount, **operation_data)


def team_bonus_handler(request, **kwargs):
    member = kwargs.get("member", None)
    pack = kwargs.get("pack", None)

    print("pack => {}".format(pack))

    ancestors_bv_update(member, pack.bv, "team_bonus")


def maintenance_incentive_handler(request, pack_id):
    maintenance_pack = MaintenancePack.objects.get(id = pack_id)

    operation_data = {
        'member': request.user.member,
        'wallet': "wallet2",
        'sender': request.user.member,
        'receiver': None,
        'operation': 'maintenance_incentive',
        'created_by': request.user.member
    }

    ancestors_bv_update(request.user.member, maintenance_pack.bv, operation = "maintenance_incentive")

    return operation_tnx("m2M", maintenance_pack.price, **operation_data)
