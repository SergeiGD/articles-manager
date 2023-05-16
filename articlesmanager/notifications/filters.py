import django_filters
from .models import Notification


class NotificationFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('date_created', 'Дата получения'),
            ('checked', 'прочитано'),
        ),
    )

    class Meta:
        model = Notification
        fields = ['subject', 'checked']

