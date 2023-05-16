import django_filters
from django.utils import timezone
from .models import Voting
from django.db import models
from django import forms


class VotingFilter(django_filters.FilterSet):

    STATUS_CHOICES = (
        (0, 'Ожидает начала'),
        (1, 'В процессе'),
        (2, 'Завершено'),
    )

    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES, method='filter_by_status', label='Статус')

    o = django_filters.OrderingFilter(
        fields=(
            ('article__name', 'Статья'),
            ('date_start', 'Начало'),
            ('date_end', 'Конец'),
        ),
    )

    # date_start__lt = django_filters.DateFromToRangeFilter(field_name='date_start', lookup_expr='lt',
    #                                         widget=forms.DateTimeField())
    #
    # date_start__gt = django_filters.DateTimeFilter(field_name='date_start', lookup_expr='gt',
    #                                                widget=forms.DateTimeField())


    class Meta:
        model = Voting
        fields = {
            'article__name': ['icontains'],
            'date_start': ['gt', 'lt'],
            'date_end': ['gt', 'lt'],
        }

        # filter_overrides = {
        #     models.DateTimeField: {
        #         # 'date_start': django_filters.DateTimeFilter,
        #         'date_start__gt': django_filters.IsoDateTimeFilter
        #     },
        # }

    def filter_by_status(self, queryset, name, value):
        if value == '0':
            return queryset.filter(date_start__lt=timezone.now())
        if value == '1':
            return queryset.filter(date_end__gte=timezone.now(), date_start__gte=timezone.now())
        return queryset.filter(date_end__lt=timezone.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['date_start__gt'].widget = forms.DateTimeInput(attrs={'type':'datetime-local'})
        self.form.fields['date_start__lt'].widget = forms.DateTimeInput(attrs={'type':'datetime-local'})
        self.form.fields['date_end__gt'].widget = forms.DateTimeInput(attrs={'type':'datetime-local'})
        self.form.fields['date_end__lt'].widget = forms.DateTimeInput(attrs={'type':'datetime-local'})
