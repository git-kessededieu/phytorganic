import random
import string

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import F

from backend import logger
from backend.models import Pack, Member, MemberBV, OperationType, MemberCounter
from backend.transactions import bv_tnx_handler
from wallet.models import MemberWallet


def generate_password(size = 8, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def member_status_update(member, status):
    """MEMBER UPDATE"""
    member_update = Member.objects.get(id = member.id)
    member_update.status = status
    member_update.save()

    """USER UPDATE"""
    user_update = User.objects.get(id = member.user.id)
    user_update.is_active = status
    user_update.save()


def member_wallet_init(member):
    """MEMBER WALLET INIT"""
    try:
        member_wallet = MemberWallet.objects.get(member = member)
    except MemberWallet.DoesNotExist as e:
        logger.info(e)
        member_wallet = MemberWallet(member = member)

    try:
        member_wallet.save()
        return member_wallet
    except IntegrityError as e:
        logger.error(e)
        return False
    except ValueError as e:
        logger.error(e)
        return False


def member_bv_init(member):
    """MEMBER BVS INIT"""
    try:
        member_bv = MemberBV.objects.get(member = member)
    except MemberBV.DoesNotExist as e:
        logger.info(e)
        member_bv = MemberBV(member = member)

    try:
        member_bv.save()
        return member_bv
    except IntegrityError as e:
        logger.error(e)
        return False
    except ValueError as e:
        logger.error(e)
        return False


def member_bv_update(member, side, bv, sender, origin):
    """MEMBER BVs UPDATE"""
    member_bv_init(member)
    member_bv = MemberBV.objects.get(member = member)
    # side = sender.placement_mode
    if side == "left":
        member_bv.left = F("left") + bv
    else:
        member_bv.right = F("right") + bv

    try:
        member_bv.save()
        bv_tnx_handler(member = member, bv = bv, side = side, sender = sender, origin = origin)
        return True
    except IntegrityError as e:
        logger.error(e)
        return False
    except ValueError as e:
        logger.error(e)
        return False


def ancestors_bv_update(member, bv, operation):
    """TEAM BVs UPDATE"""
    ancestors = member.get_ancestors(ascending = True, include_self = True)
    origin = OperationType.objects.filter(code_name = operation).first()
    [print("Active Ancestor => {}".format(ancestor.parent)) for ancestor in ancestors if
     ancestor.parent is not None and ancestor.parent.status]
    [member_bv_update(ancestor.parent, ancestor.placement_mode, bv, member, origin) for ancestor in ancestors if
     ancestor.parent is not None and ancestor.parent.status]


def set_counter(member, counter):
    try:
        member_counter = MemberCounter.objects.get(member = member, counter = counter)
    except MemberCounter.DoesNotExist as e:
        logger.info(e)
        member_counter = MemberCounter()
        member_counter.member = member
        member_counter.counter = counter

    member_counter.save()
    return member_counter


def member_leadership_init(member):
    pass


def get_bv_from_pack():
    packs = Pack.objects.all()


def overtop_handler(request, **kwargs):
    sponsor = kwargs.get("sponsor", None)
    user = kwargs.get("user", None)


def leadership_matching_handler(request, **kwargs):
    user = kwargs.get("user", None)


def autoship_bonus_handler(request, **kwargs):
    pass
