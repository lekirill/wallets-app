import django_filters.rest_framework as django_filters
from django.utils import timezone

from app.models import Transaction


class DateToFilter(django_filters.DateFilter):

    def filter(self, qs, value):
        if value:
            value = value + timezone.timedelta(days=1)
        return super(DateToFilter, self).filter(qs, value)


class FilterTransactions(django_filters.FilterSet):
    wallet_id = django_filters.NumberFilter(field_name='wallet__pk')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = DateToFilter(field_name='created_at', lookup_expr='lt')

    class Meta:
        model = Transaction
        fields = ('wallet_id', 'date_from', 'date_to',)
