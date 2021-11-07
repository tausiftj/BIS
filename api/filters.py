from django.db.models import lookups
import django_filters

from api.models import(
    CarCity
)

class CarCityFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='car__model__brand__name', lookup_expr='icontains')
    model = django_filters.CharFilter(field_name='car__model__name', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='car__model__type', lookup_expr='icontains')
    rc_no = django_filters.CharFilter(field_name='car__name', lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CarCity
        fields = ['brand', 'model', 'type', 'rc_no', 'city']