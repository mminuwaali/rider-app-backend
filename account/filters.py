from .models import Rider
from django.db import models
from django_filters import rest_framework as filters

class RiderFilter(filters.FilterSet):
    service_type = filters.CharFilter(method='filter_service_type')

    class Meta:
        model = Rider
        fields = ['service_type']

    def filter_service_type(self, queryset, name, value):
        return queryset.filter(models.Q(service_type=value) | models.Q(service_type='both'))
