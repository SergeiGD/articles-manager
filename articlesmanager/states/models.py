from django.db import models
from django.utils import timezone


class State(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')
