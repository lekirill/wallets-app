from decimal import Decimal
from django.test import TestCase
from rest_framework import status

from app.models import Wallet, Transaction


class TransactionApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.wallet = Wallet.objects.create(label='test_wallet')
        cls.transaction_1 = Transaction.objects.create(wallet=cls.wallet, amount=Decimal('100.00'))
        cls.transaction_1 = Transaction.objects.create(wallet=cls.wallet, amount=Decimal('-100.00'))
        cls.transaction_1 = Transaction.objects.create(wallet=cls.wallet, amount=Decimal('50.00'))

    def test_transaction_list_ok(self):
        response = self.client.get('/v1/transaction/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['count'] == 3
        assert list(data['results'][0].keys()) == ['id', 'amount', 'txid', 'wallet']

    def test_transaction_retrieve_ok(self):
        response = self.client.get(f'/v1/transaction/{self.transaction_1.txid}')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == {
            'amount': str(self.transaction_1.amount),
            'id': self.transaction_1.pk,
            'txid': self.transaction_1.txid,
            'wallet': self.transaction_1.wallet_id
        }

    def test_transaction_retrieve_not_found(self):
        response = self.client.get(f'/v1/transaction/{"random_tx_id"}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
