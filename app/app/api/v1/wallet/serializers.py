from decimal import Decimal
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance']


class CreateUpdateWalletRequestSerializer(serializers.Serializer):
    label = serializers.CharField(required=True)

    def validate_label(self, label):
        if Wallet.objects.filter(label=label).exists():
            raise ValidationError({'label': 'Wallet with that label already exists'})
        return label


class WalletDepositWithdrawRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=18, decimal_places=2, min_value=Decimal(0), required=True)
    wallet_id = serializers.IntegerField(required=True)

    def validate_wallet_id(self, wallet_id):
        if not Wallet.objects.filter(pk=wallet_id).exists():
            raise ValidationError('Such wallet does not exist')
        return wallet_id
