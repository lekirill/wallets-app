import logging
from contextlib import contextmanager
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from typing import ContextManager

from app.models import Transaction
from app.api.v1.transaction.serializers import TransactionSerializer
from app.api.v1.transaction.filters import FilterTransactions

logger = logging.getLogger(__name__)


class TransactionAPIView(ListAPIView, APIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = FilterTransactions
    filter_backends = [DjangoFilterBackend, ]

    @swagger_auto_schema(
        tags=['transaction'],
        operation_summary='Transaction list',
        responses={
            status.HTTP_200_OK: TransactionSerializer()
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TransactionRetrieveAPIView(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Transaction, txid=kwargs['txid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['transaction'],
        operation_summary='Get transaction by txid',
        responses={
            status.HTTP_200_OK: TransactionSerializer(),
            status.HTTP_404_NOT_FOUND: 'Not found',
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
