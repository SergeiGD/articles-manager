from django.db import models
from django.urls import reverse

from users.models import CustomUser
from django.utils import timezone


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
    date_voted = models.DateTimeField(verbose_name='Дата голоса', default=timezone.now)
    date_changed = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')


class Voting(models.Model):
    article = models.ForeignKey(
        to='articles.Article',
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

    @property
    def count_votes(self):
        return self.users.count()

    @property
    def count_agreed(self):
        return self.users.filter(votingusers__agreed=True).count()

    @property
    def count_disagreed(self):
        return self.users.filter(votingusers__agreed=False).count()

    @property
    def status(self):
        if self.date_start < timezone.now():
            return 'Ожидает начала'
        if self.date_end > timezone.now():
            return 'В процессе'
        return 'Завершено'

    class Meta:
        ordering = ['-date_start', ]

    def get_agreed_url(self):
        return reverse('votings_agreed', kwargs={'pk': self.pk})

    def get_disagreed_url(self):
        return reverse('votings_disagreed', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse('votings_detail', kwargs={'pk': self.pk})