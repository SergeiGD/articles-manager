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

    def get_articles_to_review(self):
        result = []
        user_articles = self.articles.filter(
            is_ready_to_votings=False,
            date_deleted=None,
            users__in=[self],
        ).all()
        for article in user_articles:
            if not article.reviews.filter(
                user=self,
                date_created__gt=article.date_repulished,
            ).exists():
                result.append(article)

        return result

    def can_create_review(self, article):
        if article.date_deleted is not None or article.is_ready_to_votings:
            return False

        if self not in article.users.all():
            return False

        if article.reviews.filter(
            user=self,
            date_created__gt=article.date_repulished
        ).exists():
            return False

        return True

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


@receiver(pre_save, sender=CustomUser)
def author_pre_save(sender, instance, **kwargs):
    instance.date_edited = timezone.now()

@receiver(pre_save, sender=Position)
def author_pre_save(sender, instance, **kwargs):
    instance.date_edited = timezone.now()
