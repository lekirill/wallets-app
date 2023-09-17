from decimal import Decimal
from django.db import transaction

from app.exceptions import InsufficientFunds
from app.models import Wallet


def deposit_process(wallet_id: int, amount: Decimal):
    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=wallet_id)
        wallet.balance_plus(amount=amount)


def withdraw_process(wallet_id: int, amount: Decimal):
    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=wallet_id)
        if wallet.balance - amount < 0:
            raise InsufficientFunds()
        wallet.balance_minus(amount=amount)
