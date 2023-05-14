from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Эл. почта', unique=True)
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    def get_detail_url(self):
        return reverse('detail_authors', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('update_authors', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_authors', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date_created']


@receiver(pre_save, sender=Author)
def author_pre_save(sender, instance, **kwargs):
    instance.date_edited = timezone.now()
