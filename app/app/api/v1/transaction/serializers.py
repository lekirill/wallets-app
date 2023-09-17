from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'txid', 'wallet']
