from decimal import Decimal
from django.test import TestCase

from app.exceptions import InsufficientFunds
from app.models import Wallet, Transaction
from app.utils import deposit_process, withdraw_process


class UtilsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.wallet = Wallet.objects.create(label='test_wallet')

    def test_deposit_process_ok(self):
        deposit_process(
            wallet_id=self.wallet.pk,
            amount=Decimal('100'),
        )
        self.wallet.refresh_from_db()
        assert self.wallet.balance == Decimal('100')
        assert Transaction.objects.filter(wallet=self.wallet, amount=Decimal('100')).exists()

    def test_withdraw_process_ok(self):
        deposit_process(
            wallet_id=self.wallet.pk,
            amount=Decimal('100'),
        )
        self.wallet.refresh_from_db()
        assert self.wallet.balance == Decimal('100')
        withdraw_process(
            wallet_id=self.wallet.pk,
            amount=Decimal('50'),
        )
        self.wallet.refresh_from_db()
        assert self.wallet.balance == Decimal('50')
        assert Transaction.objects.filter(wallet=self.wallet, amount=Decimal('100')).exists()
        assert Transaction.objects.filter(wallet=self.wallet, amount=Decimal('-50')).exists()

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(InsufficientFunds):
            withdraw_process(
                wallet_id=self.wallet.pk,
                amount=Decimal('50'),
            )
