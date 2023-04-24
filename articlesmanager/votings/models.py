from django.db import models
from articles.models import Article
from users.models import CustomUser


class VotingUsers(models.Model):
    voting = models.ForeignKey(
        to='Voting',
        on_delete=models.CASCADE,
        verbose_name='Голосование',
    )
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT,
        verbose_name='Пользователь',
    )
    agreed = models.BooleanField(verbose_name='Проголовал за', default=False)
    date_voted = models.DateTimeField(verbose_name='Дата голоса')
    date_changed = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')


class Voting(models.Model):
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        verbose_name='Статья',
        related_name='votings',
        related_query_name='voting',
    )
    users = models.ManyToManyField(
        through=VotingUsers,
        to=CustomUser,
        verbose_name='Пользователи',
        related_name='votings',
        related_query_name='voting',
    )
    date_start = models.DateTimeField(verbose_name='Дата начала')
    date_end = models.DateTimeField(verbose_name='Дата завершения')
