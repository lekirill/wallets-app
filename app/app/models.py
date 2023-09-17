import uuid

from decimal import Decimal
from django.db import models


class Wallet(models.Model):
    label = models.CharField(max_length=255, null=False, unique=True)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wallet'

    def balance_plus(self, amount: Decimal):
        self.change_balance(sign=Decimal('1'), amount=amount)

    def balance_minus(self, amount: Decimal):
        self.change_balance(sign=Decimal('-1'), amount=amount)

    def change_balance(self, sign: Decimal, amount: Decimal):
        new_balance = self.balance + amount * sign
        self.balance = new_balance
        transaction = Transaction()
        transaction.amount = amount * sign
        transaction.wallet = self
        transaction.save()
        self.save(update_fields=['balance', ])


class Transaction(models.Model):
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=18, decimal_places=2, null=False)
    txid = models.CharField(max_length=36, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transaction'
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.txid:
            self.txid = self.generate_txid()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_txid():
        return str(uuid.uuid4())
