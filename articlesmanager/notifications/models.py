from django.db import models
from django.utils import timezone
from users.models import CustomUser
from articles.models import Article
from votings.models import Voting


class Notification(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='notifications',
        related_query_name='notification'
    )
    voting = models.ForeignKey(
        to=Voting,
        on_delete=models.CASCADE,
        verbose_name='Голосование',
        null=True,
        blank=True,
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
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
