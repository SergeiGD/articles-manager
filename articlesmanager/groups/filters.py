import django_filters
from .models import UserGroup, GroupPermission


class GroupFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('name', 'Наименование'),
        ),
    )

    class Meta:
        model = UserGroup
        fields = {
            'name': ['icontains'],
        }


class PermissionFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('name', 'Наименование'),
            ('codename', 'Код'),
        ),
    )

    class Meta:
        model = GroupPermission
        fields = {
            'name': ['icontains'],
            'codename': ['icontains'],
        }
