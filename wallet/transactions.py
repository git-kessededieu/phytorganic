from decimal import Decimal

from django.db import IntegrityError
from django.db.models import F

from backend import logger
from backend.models import OperationType
from frontend.enums import PROCESSES
from wallet.models import MemberWalletTransactions, MemberWallet, MainWalletTransactions, MainWallet


def main_wallet_operation(amount, **data):
    main_wallet_balance = MainWallet.objects.first()
    if main_wallet_balance is None:
        main_wallet = MainWallet(balance = amount)
        main_wallet.save()
    else:
        main_wallet_balance.balance = F('balance') + amount
        main_wallet_balance.save()

    return main_wallet_tnx(amount = amount, **data)


def main_wallet_tnx(amount, **data):
    transaction_info = {
        "sender": data.get("sender", None),
        "receiver": data.get("receiver", None),
        "operation": data.get("operation", ""),
        "type": "credit" if int(amount) > 0 else "debit",
        "amount": abs(amount),
        "origin": data.get("operation_type", None),
        "created_by": data.get("created_by")
    }
    transaction = MainWalletTransactions(**transaction_info)
    try:
        transaction.save()
        return True
    except IntegrityError as e:
        logger.error(e)
        return False
    except ValueError as e:
        logger.error(e)
        return False


def member_wallet_operation(amount, **data):
    member = data.get("member", "")
    print("member => {}".format(member))
    wallet = data.get("wallet", "")
    print("wallet => {}".format(wallet))

    member_wallet = MemberWallet.objects.get(member = member)
    print("member_wallet => {}".format(member_wallet))
    if wallet == "wallet1":
        m_wallet = member_wallet.wallet1
    else:
        m_wallet = member_wallet.wallet2

    if 0 > amount > m_wallet:
        return False

    if wallet == "wallet1":
        member_wallet.wallet1 = F('wallet1') + amount
    else:
        member_wallet.wallet2 = F('wallet2') + amount
    member_wallet.save()

    return member_wallet_tnx(amount = amount, **data)


def member_wallet_tnx(amount, **data):
    transaction_info = {
        "sender": data.get("sender", None),
        "receiver": data.get("receiver", None),
        "wallet": data.get("wallet"),
        "operation": data.get("operation", ""),
        "type": "credit" if int(amount) > 0 else "debit",
        "amount": abs(amount),
        "origin": data.get("operation_type", None),
        "created_by": data.get("created_by")
    }
    print("transaction_info => {}".format(transaction_info))
    transaction = MemberWalletTransactions(**transaction_info)
    try:
        transaction.save()
        return True
    except IntegrityError as e:
        logger.error(e)
        return False
    except ValueError as e:
        logger.error(e)
        return False


def operation_tnx(process, amount, **data):
    amount = Decimal(amount)
    member = data.get("member", "")
    wallet = data.get("wallet", "")
    sender = data.get("sender", None)
    receiver = data.get("receiver", None)
    operation = data.get("operation")
    operation_type = OperationType.objects.filter(code_name = operation).first()
    created_by = data.get("created_by")
    if process in PROCESSES:
        if process == "m2m":
            tnx_1 = member_wallet_operation(amount = -amount, member = sender, sender = sender,
                                            receiver = receiver, wallet = wallet, operation = operation,
                                            operation_type = operation_type, created_by = created_by)
            tnx_2 = member_wallet_operation(amount = amount, member = receiver, sender = sender,
                                            receiver = receiver, wallet = "wallet2", operation = operation,
                                            operation_type = operation_type, created_by = created_by)
            if tnx_1 and tnx_2:
                return True
            else:
                return False
        elif process == "m2M":
            tnx_1 = member_wallet_operation(amount = -amount, member = member, sender = sender,
                                            receiver = receiver, wallet = wallet, operation = operation,
                                            operation_type = operation_type, created_by = created_by)

            tnx_2 = main_wallet_operation(amount = amount, member = member, sender = sender,
                                          receiver = receiver, operation = operation, operation_type = operation_type,
                                          created_by = created_by)
            if tnx_1 and tnx_2:
                return True
            else:
                return False
        elif process == "M2m":
            tnx_1 = main_wallet_operation(amount = -amount, member = member, sender = sender,
                                          receiver = receiver, operation = operation, operation_type = operation_type,
                                          created_by = created_by)

            tnx_2 = member_wallet_operation(amount = amount, member = member, sender = sender,
                                            receiver = receiver, wallet = wallet, operation = operation,
                                            operation_type = operation_type, created_by = created_by)
            if tnx_1 and tnx_2:
                return True
            else:
                return False
        else:
            return False
    return False
