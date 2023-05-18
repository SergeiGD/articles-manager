from django.db import models
from django.urls import reverse
from django.utils import timezone


class State(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    def get_update_url(self):
        return reverse('update_states', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse('detail_states', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_states', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date_created']
        permissions = (
            ("добавление_статусов", "Добавление статусов"),
            ("изменение_статусов", "Изменение статусов"),
            ("удаление_статусов", "Удаление статусов"),
        )
