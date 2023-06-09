from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.core.validators import RegexValidator
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, verbose_name='Имя', validators=[
        RegexValidator('^([^0-9]*)$')
    ])
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', validators=[
        RegexValidator('^([^0-9]*)$')
    ])
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество', validators=[
        RegexValidator('^([^0-9]*)$')
    ])
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

    def get_notifications_count(self):
        return self.notifications.filter(checked=False).count()


    def get_detail_url(self):
        return reverse('detail_users', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('update_users', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_users', kwargs={'pk': self.pk})

    def get_reset_password_url(self):
        return reverse('reset_user_password', kwargs={'pk': self.pk})

    def get_select_group_url(self):
        return reverse('select_group_for_user', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date_created']
        permissions = (
            ("добавление_пользователей", "Добавление пользователей"),
            ("изменение_пользователей", "Изменение пользователей"),
            ("удаление_пользователей", "Удаление пользователей"),
        )


class Position(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse('update_positions', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_positions', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse('detail_positions', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date_created']
        permissions = (
            ("добавление_должностей", "Добавление должностей"),
            ("изменение_должностей", "Изменение должностей"),
            ("удаление_должностей", "Удаление должностей"),
        )


@receiver(pre_save, sender=CustomUser)
def author_pre_save(sender, instance, **kwargs):
    instance.date_edited = timezone.now()

@receiver(pre_save, sender=Position)
def author_pre_save(sender, instance, **kwargs):
    instance.date_edited = timezone.now()
