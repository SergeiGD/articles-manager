from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Отчество')
    email = models.EmailField(
        verbose_name='Эл. почта',
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    position = models.ForeignKey(
        to='Position',
        on_delete=models.PROTECT,
        verbose_name='Должность',
    )
    objects = CustomUserManager()
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    def get_articles_to_review(self):
        print('asdasdd')
        print('asdasdd')

        return self.articles.filter(is_ready_to_votings=False, date_deleted=None)


class Position(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    def __str__(self):
        return self.name


@receiver(pre_save, sender=CustomUser)
def author_pre_save(sender, instance, **kwargs):
    instance.date_edited = timezone.now()

@receiver(pre_save, sender=Position)
def author_pre_save(sender, instance, **kwargs):
    instance.date_edited = timezone.now()
