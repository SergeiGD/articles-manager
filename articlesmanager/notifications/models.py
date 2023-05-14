from django.db import models
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
        ARTICLE_REPUBLISHED = "ARTICLE_REPUBLISHED", _("Внесены правки в статью")
        REVIEWER = "REVIEWER", _("Вы назначены рецензентом")
        VOTING = "VOTING", _("Началось голосование")
    #     SENIOR = "SR", _("Senior")
    #     GRADUATE = "GR", _("Graduate")
    # SUBJECT_CHOICES = (
    #     ("ARTICLE_REPUBLISHED", "Внесены правки в статью"),
    #     ("REVIEWER", "Вы назначены рецензентом"),
    #     ("VOTING", "Началось голосование"),
    # )
    subject = models.CharField(choices=NotificationsSubjects.choices, verbose_name='Тема', null=True)
    content = models.TextField(verbose_name='Содержание', null=True)
    checked = models.BooleanField(default=False, verbose_name='Просмотрено')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

