import django_filters
from articles.models import Article


class ArticlesToReviewFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('name', 'Наименование'),
        ),
    )

    class Meta:
        model = Article
        fields = {
            'name': ['icontains'],
        }
