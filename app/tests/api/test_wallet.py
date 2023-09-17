from decimal import Decimal
from django.db.models import Sum
from django.test import TestCase
from rest_framework import status

from app.models import Wallet, Transaction


class WalletnApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(3):
            Wallet.objects.create(label=f'test_wallet_{i}')

    def test_wallets_list_ok(self):
        response = self.client.get('/v1/wallet/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['count'] == 3
        assert list(data['results'][0].keys()) == ['id', 'label', 'balance']

    def test_wallet_create_has_wallet_w_same_label(self):
        response = self.client.post('/v1/wallet/', data={'label': Wallet.objects.last().label})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data == {'label': {'label': 'Wallet with that label already exists'}}

    def test_wallet_create_ok(self):
        response = self.client.post('/v1/wallet/', data={'label': 'new_test_label'})
        assert response.status_code == status.HTTP_201_CREATED
        assert Wallet.objects.filter(label='new_test_label').exists()

    def test_wallet_retrieve_ok(self):
        wallet = Wallet.objects.last()
        response = self.client.get(f'/v1/wallet/{wallet.pk}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == {'balance': str(wallet.balance), 'id': wallet.pk, 'label': wallet.label}

    def test_wallet_retrieve_not_found(self):
        response = self.client.get(f'/v1/wallet/{666}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_wallet_update_label_ok(self):
        wallet = Wallet.objects.last()
        response = self.client.patch(
            f'/v1/wallet/{wallet.pk}/',
            data={'label': 'new test label'},
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == {'balance': str(wallet.balance), 'id': wallet.pk, 'label': 'new test label'}

    def test_wallet_update_label_not_dound(self):
        response = self.client.patch(
            f'/v1/wallet/{666}/',
            data={'label': 'new test label'},
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_wallet_deposit_ok(self):
        wallet = Wallet.objects.last()
        old_balance = wallet.balance
        response = self.client.post(
            f'/v1/wallet/deposit/',
            data={'amount': Decimal('100'), 'wallet_id': wallet.pk},
        )
        assert response.status_code == status.HTTP_201_CREATED
        wallet.refresh_from_db()
        assert wallet.balance == old_balance + Decimal('100')

    def test_wallet_deposit_no_wallet(self):
        response = self.client.post(
            f'/v1/wallet/deposit/',
            data={'amount': Decimal('100'), 'wallet_id': 666},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data == {'wallet_id': ['Such wallet does not exist']}

    def test_wallet_withdraw_ok(self):
        wallet = Wallet.objects.last()
        old_balance = Decimal('1000')
        wallet.balance = old_balance
        wallet.save(update_fields=['balance', ])
        response = self.client.post(
            f'/v1/wallet/withdraw/',
            data={'amount': Decimal('10'), 'wallet_id': wallet.pk},
        )
        assert response.status_code == status.HTTP_201_CREATED
        wallet.refresh_from_db()
        assert wallet.balance == old_balance - Decimal('10')

    def test_wallet_withdraw_no_funds(self):
        wallet = Wallet.objects.last()
        old_balance = Decimal('0')
        wallet.balance = old_balance
        wallet.save(update_fields=['balance', ])
        response = self.client.post(
            f'/v1/wallet/withdraw/',
            data={'amount': Decimal('90'), 'wallet_id': wallet.pk},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data == {'amount': 'Not enough funds to make withdrawal'}

    def test_wallet_withdraw_no_wallet(self):
        response = self.client.post(
            f'/v1/wallet/withdraw/',
            data={'amount': Decimal('50'), 'wallet_id': 777},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data == {'wallet_id': ['Such wallet does not exist']}

    def test_balance_transaction_amount(self):
        wallet = Wallet.objects.first()
        self.client.post(f'/v1/wallet/deposit/', data={'amount': Decimal('1000'), 'wallet_id': wallet.pk})
        self.client.post(f'/v1/wallet/deposit/', data={'amount': Decimal('99'), 'wallet_id': wallet.pk})
        self.client.post(f'/v1/wallet/deposit/', data={'amount': Decimal('40'), 'wallet_id': wallet.pk})
        self.client.post(f'/v1/wallet/withdraw/', data={'amount': Decimal('14'), 'wallet_id': wallet.pk})
        self.client.post(f'/v1/wallet/withdraw/', data={'amount': Decimal('2000'), 'wallet_id': wallet.pk})
        wallet.refresh_from_db()
        transactions_sum_amount = Transaction.objects.filter(wallet=wallet).aggregate(Sum('amount'))
        assert wallet.balance == transactions_sum_amount['amount__sum']
