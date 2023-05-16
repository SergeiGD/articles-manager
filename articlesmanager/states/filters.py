import django_filters
from .models import State


class StateFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('name', 'Наименование'),
        ),
    )

    class Meta:
        model = State
        fields = {
            'name': ['icontains'],
        }
