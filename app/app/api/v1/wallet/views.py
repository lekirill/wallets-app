import logging
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response

from app.exceptions import InsufficientFunds
from app.models import Wallet
from app.settings import OPERATION_LOCK_TIME_SEC
from app.utils import deposit_process, withdraw_process
from app.api.v1.wallet.filters import FilterWallets
from app.api.v1.wallet.serializers import (
    WalletSerializer,
    CreateUpdateWalletRequestSerializer,
    WalletDepositWithdrawRequestSerializer,
)

logger = logging.getLogger(__name__)


class WalletAPIView(ListAPIView, APIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_class = FilterWallets
    filter_backends = [DjangoFilterBackend, ]

    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Wallet list',
        responses={
            status.HTTP_200_OK: WalletSerializer()
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Create wallet',
        request_body=CreateUpdateWalletRequestSerializer(),
        as_form_body=True,
        responses={
            status.HTTP_201_CREATED: WalletSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Invalid data',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateUpdateWalletRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        wallet = Wallet()
        wallet.label = data['label']
        wallet.save()
        response_serializer = WalletSerializer(wallet, read_only=True)

        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)


class WalletRetrieveAPIView(RetrieveAPIView, UpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Get wallet',
        responses={
            status.HTTP_200_OK: WalletSerializer(),
            status.HTTP_404_NOT_FOUND: 'Not found',
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Update wallet\'s label',
        request_body=CreateUpdateWalletRequestSerializer,
        as_form_body=True,
        responses={
            status.HTTP_204_NO_CONTENT: WalletSerializer(),
            status.HTTP_404_NOT_FOUND: 'Not found',
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class WalletDepositAPIView(APIView):

    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Deposit to wallet',
        request_body=WalletDepositWithdrawRequestSerializer(),
        as_form_body=True,
        responses={
            status.HTTP_201_CREATED: 'Created',
            status.HTTP_204_NO_CONTENT: 'Awaiting',
            status.HTTP_400_BAD_REQUEST: 'Invalid data',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = WalletDepositWithdrawRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        lock_acquired = cache.add(
            f'deposit:{data["wallet_id"]}:{str(data["amount"])}',
            'locked',
            OPERATION_LOCK_TIME_SEC
        )
        if lock_acquired:
            deposit_process(wallet_id=data['wallet_id'], amount=data['amount'])

            return Response(data='Created', status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class WalletWithdrawAPIView(APIView):

    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Withdraw from wallet',
        request_body=WalletDepositWithdrawRequestSerializer(),
        as_form_body=True,
        responses={
            status.HTTP_201_CREATED: 'Created',
            status.HTTP_204_NO_CONTENT: 'Awaiting',
            status.HTTP_400_BAD_REQUEST: 'Invalid data',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = WalletDepositWithdrawRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        lock_acquired = cache.add(
            f'withdrawal:{data["wallet_id"]}:{str(data["amount"])}',
            'locked',
            OPERATION_LOCK_TIME_SEC
        )
        if lock_acquired:
            try:
                withdraw_process(wallet_id=data['wallet_id'], amount=data['amount'])
            except InsufficientFunds:
                raise ValidationError({'amount': 'Not enough funds to make withdrawal'})

            return Response(data='Created', status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
