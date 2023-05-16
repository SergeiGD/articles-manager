from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import CustomUser
from articles.models import Article
from votings.models import Voting
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='notifications',
        related_query_name='notification'
    )
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Статья',
        related_name='notifications',
        related_query_name='notification'
    )

    class NotificationsSubjects(models.TextChoices):
        ARTICLE_REPUBLISHED = "Внесены правки в статью", _("Внесены правки в статью")
        REVIEWER = "Вы назначены рецензентом", _("Вы назначены рецензентом")
        VOTING = "Назначено голосование", _("Назначено голосование")

    subject = models.CharField(choices=NotificationsSubjects.choices, verbose_name='Тема', null=True)
    content = models.TextField(verbose_name='Содержание', null=True)
    checked = models.BooleanField(default=False, verbose_name='Просмотрено')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def get_detail_url(self):
        return reverse('detail_notifications', kwargs={'pk': self.pk})

    def get_checked_url(self):
        return reverse('mark_as_checked', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_notifications', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['checked', '-date_created']

