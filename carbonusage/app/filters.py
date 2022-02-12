from codecs import lookup_error
from django_filters import rest_framework as filters
from .models import Usage

class UsageFilter(filters.FilterSet):
    usage_at_start_date = filters.DateTimeFilter(field_name='usage_at', lookup_expr='gte')
    usage_at_end_date = filters.DateTimeFilter(field_name='usage_at', lookup_expr='lte')

    class Meta:
        model = Usage
        fields = ['usage_at_start_date', 'usage_at_end_date']