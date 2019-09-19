from django.db import IntegrityError

from backend import logger
from backend.models import OrderInfo, MemberBVHistory


def order_tnx_handler(**data):
    member = data.get("member")
    order_type = data.get("order_type")
    pack = data.get("pack")
    payment_mode = data.get("payment_mode")
    delivery_method = data.get("delivery_method")

    new_order = OrderInfo()
    new_order.member = member
    new_order.order_type = order_type
    new_order.pack = None if pack is None else pack.id
    new_order.payment_mode = payment_mode
    new_order.delivery_method = delivery_method
    try:
        new_order.save()
        print("new_order => {}".format(new_order.pack))
        return True
    except IntegrityError as e:
        logger.error(e)
        return False
    except ValueError as e:
        logger.error(e)
        return False


def bv_tnx_handler(**data):
    transaction_info = {
        "member": data.get("member"),
        "bv": data.get("bv"),
        "side": data.get("side"),
        "sender": data.get("sender"),
        "origin": data.get("origin")
    }
    transaction = MemberBVHistory(**transaction_info)
    try:
        transaction.save()
        return True
    except IntegrityError as e:
        logger.error(e)
        return False
    except ValueError as e:
        logger.error(e)
        return False
