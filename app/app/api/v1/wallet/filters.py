import django_filters.rest_framework as django_filters
from django.utils import timezone

from app.models import Wallet


class DateToFilter(django_filters.DateFilter):

    def filter(self, qs, value):
        if value:
            value = value + timezone.timedelta(days=1)
        return super(DateToFilter, self).filter(qs, value)


class FilterWallets(django_filters.FilterSet):
    balance_from = django_filters.NumberFilter(field_name='balance', lookup_expr='gte')
    balance_to = django_filters.NumberFilter(field_name='balance', lookup_expr='lte')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = DateToFilter(field_name='created_at', lookup_expr='lt')

    class Meta:
        model = Wallet
        fields = ('balance_from', 'balance_to', 'date_from', 'date_to',)
