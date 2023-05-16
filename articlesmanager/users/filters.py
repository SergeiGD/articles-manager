import django_filters
from .models import CustomUser, Position


class CustomUserFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('first_name', 'Имя'),
            ('last_name', 'Фамилия'),
            ('email', 'Email'),
        ),
    )

    class Meta:
        model = CustomUser
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'middle_name': ['icontains'],
            'email': ['icontains'],
        }


class PositionFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('name', 'Наименование'),
        ),
    )

    class Meta:
        model = Position
        fields = {
            'name': ['icontains'],
        }
