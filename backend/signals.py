from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from backend import logger
from backend.methods import generate_password
from backend.models import Member, MemberBV, Leadership
from phytorganic.notify import notifier
from wallet.models import MemberWalletTransactions, MemberWallet


@receiver(post_save, sender = MemberWalletTransactions)
def add_reference(sender, instance, created, **kwargs):
    # instance.set_password(instance.password)
    pass


@receiver(pre_save, sender = Member)
def pre_save_member(sender, instance, **kwargs):
    num = Member.objects.filter(pk = instance.pk).count()
    parent = Member.objects.filter(username = instance.placement_name).first()
    if num == 0:
        instance.parent = parent


@receiver(post_save, sender = Member)
def create_user(sender, instance, created, **kwargs):
    """MEMBER USER'INFO INIT"""
    if created:
        password = generate_password()
        user_info = {
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'password': make_password(password),
            'is_active': True
        }

        try:
            user = User.objects.get(username = instance.username)
            user.set_password(password)
        except User.DoesNotExist as e:
            logger.info(e)
            user = User(**user_info)
        user.save()

        instance.user = user

        notify_data = {
            'action': 'creation',
            'e_subject': 'PhytOrganic - Member Creation',
            'e_receiver': instance.email,
            'e_context': {'username': instance.username, 'password': password}
        }
        notifier(**notify_data)

        instance.save()


@receiver(post_save, sender = Member)
def member_wallet_init(sender, instance, created, **kwargs):
    """MEMBER WALLET INIT"""
    if created:
        try:
            member_wallet = MemberWallet.objects.get(member = instance)
        except MemberWallet.DoesNotExist as e:
            logger.info(e)
            member_wallet = MemberWallet(member = instance)

        try:
            member_wallet.save()
        except IntegrityError as e:
            logger.error(e)
        except ValueError as e:
            logger.error(e)


@receiver(post_save, sender = Member)
def member_bv_init(sender, instance, created, **kwargs):
    """MEMBER BVS INIT"""
    if created:
        try:
            member_bv = MemberBV.objects.get(member = instance)
        except MemberBV.DoesNotExist as e:
            logger.info(e)
            member_bv = MemberBV(member = instance)

        try:
            member_bv.save()
        except IntegrityError as e:
            logger.error(e)
        except ValueError as e:
            logger.error(e)


@receiver(post_save, sender = Member)
def member_leadership_status(sender, instance, created, **kwargs):
    """MEMBER LEADERSHIP STATUS"""
    if created:
        if instance.leadership is None:
            leadership_status = Leadership.objects.filter(code = 'L').first()
            instance.leadership = None if leadership_status is None else leadership_status
            instance.save()
