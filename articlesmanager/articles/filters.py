import django_filters
from .models import Article
from django.forms import forms



class ArticleFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('name', 'Наименование'),
            ('date_created', 'Дата создания'),
            ('date_repulished', 'Дата внесения правок'),
        ),
    )

    class Meta:
        model = Article
        fields = {
            'unique': ['lt', 'gt'],
            'name': ['icontains'],
            'quoting': ['lt', 'gt'],
        }
