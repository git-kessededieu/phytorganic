from decimal import Decimal

from django.db import IntegrityError
from django.db.models import F

from backend import logger
from backend.models import Member, MemberBV
from frontend.enums import MAINTENANCE_PARING_PERCENT
from wallet.transactions import operation_tnx


def maintenance_pairing(*args, **kwargs):
    """print('ARGS => {}'.format(args))
    print('KWARGS => {}'.format(kwargs))
    member = kwargs.get('member', None)
    limit = kwargs.get('limit')"""
    members = Member.objects.filter(status = True)
    for member in members:
        if member is not None and member.status is True:
            left = member.member_bv.left
            right = member.member_bv.right

            bv = right if left - right >= 0 else left

            if bv > 0:
                amount = bv * (MAINTENANCE_PARING_PERCENT / 100) * 2

                operation_data = {
                    'member': member,
                    'wallet': 'wallet1',
                    'receiver': member,
                    'operation': 'maintenance_pairing',
                    'created_by': member
                }
                transaction_status = operation_tnx("M2m", Decimal(amount), **operation_data)
                if transaction_status:
                    member_bv = MemberBV.objects.get(member = member)
                    member_bv.left = F("left") - bv
                    member_bv.right = F("right") - bv

                    try:
                        member_bv.save()
                        return True
                    except IntegrityError as e:
                        logger.error(e)
                        return False
                    except ValueError as e:
                        logger.error(e)
                        return False
            else:
                return False
        else:
            return False


def team_bonus(*args, **kwargs):
    member = kwargs.get("member", None)
    limit = kwargs.get("limit")
    members = Member.objects.filter(status = True)[:limit]
    for member in members:
        if member is not None and member.status is True:
            left = member.member_bv.left
            right = member.member_bv.right

            bv = right if left - right >= 0 else left

            if bv > 0:
                amount = bv * (MAINTENANCE_PARING_PERCENT / 100) * 2

                operation_data = {
                    'member': member,
                    'wallet': 'wallet1',
                    'receiver': member,
                    'operation': 'maintenance_pairing',
                    'created_by': member
                }
                transaction_status = operation_tnx("M2m", Decimal(amount), **operation_data)
                if transaction_status:
                    member_bv = MemberBV.objects.get(member = member)
                    member_bv.left = F("left") - bv
                    member_bv.right = F("right") - bv

                    try:
                        member_bv.save()
                        return True
                    except IntegrityError as e:
                        logger.error(e)
                        return False
                    except ValueError as e:
                        logger.error(e)
                        return False
            else:
                return False
        else:
            return False
