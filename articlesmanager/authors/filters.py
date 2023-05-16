import django_filters
from .models import Author


class AuthorFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('first_name', 'Имя'),
            ('last_name', 'Фамилия'),
            ('email', 'Email'),
        ),
    )

    class Meta:
        model = Author
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'middle_name': ['icontains'],
            'email': ['icontains'],
        }
