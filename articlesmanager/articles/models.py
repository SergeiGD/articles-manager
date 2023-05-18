import uuid

from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from authors.models import Author
from states.models import State
from users.models import CustomUser
from votings.models import Voting


def build_photo_path(instance, filename):
    """
    генерация пути для фотографий
    """
    ext = filename.split('.')[-1]
    code = uuid.uuid4()
    return '{0}.{1}'.format(code, ext)


class ArticleState(models.Model):
    article = models.ForeignKey(
        to='Article',
        on_delete=models.CASCADE,
        verbose_name='Статья',
    )
    state = models.ForeignKey(
        to=State,
        on_delete=models.CASCADE,
        verbose_name='Статус',
    )
    date_set = models.DateTimeField(default=timezone.now, verbose_name='Дата присвоения')



class Article(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    file = models.FileField(verbose_name='Файл', upload_to=build_photo_path)
    unique = models.FloatField(verbose_name='Оригинальность', validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    bibliography = models.TextField(verbose_name='Библиография')
    quoting = models.FloatField(verbose_name='Степень цитирования', validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    authors = models.ManyToManyField(
        verbose_name='Авторы',
        related_name='articles',
        related_query_name='article',
        to=Author,
    )
    states = models.ManyToManyField(
        through=ArticleState,
        to=State,
        related_name='articles',
        related_query_name='article'
    )
    users = models.ManyToManyField(
        verbose_name='Проверяющие',
        related_name='articles',
        related_query_name='article',
        to=CustomUser,
    )
    is_ready_to_votings = models.BooleanField(default=False, verbose_name='Готова к голосованию')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')
    date_repulished = models.DateTimeField(default=timezone.now, verbose_name='Дата внесения правок')

    class Meta:
        ordering = ['-date_created']
        permissions = (
            ("добавление_статьей", "Добавление статьей"),
            ("изменение_статьей", "Изменение статей"),
            ("удаление_статьей", "Удаление статей"),
        )

    def get_current_state(self):
        return self.states.filter(
            articlestate__date_set=self.states.aggregate(max_date=Max('articlestate__date_set'))['max_date']
        ).first()

    def save(self, *args, **kwargs):
        self.date_edited = timezone.now()
        super().save(*args, **kwargs)

    @property
    def count_approved(self):
        return self.reviews.filter(
            date_created__gt=self.date_repulished,
            approved=True,
            user__in=self.users.all(),
        ).count()

    @property
    def count_unapproved(self):
        return self.reviews.filter(
            date_created__gt=self.date_repulished,
            approved=False,
            user__in=self.users.all(),
        ).count()

    @property
    def enable_for_votings(self):

        if self.votings.exists():
            return False

        if self.is_ready_to_votings:
            return True

        if self.reviews.filter(
            date_created__gt=self.date_repulished,
        ).count() < self.users.filter(date_deleted=None).count():
            return False

        if self.count_approved <= self.count_unapproved:
            return False

        return True

    def get_update_url(self):
        return reverse('update_articles', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_articles', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse('detail_articles', kwargs={'pk': self.pk})

    def get_download_url(self):
        return reverse('download_articles', kwargs={'pk': self.pk})

    def get_select_author_url(self):
        return reverse('select_author', kwargs={'pk': self.pk})

    def get_select_user_url(self):
        return reverse('select_user_for_article', kwargs={'pk': self.pk})

    def get_create_review_url(self):
        return reverse('create_review', kwargs={'pk': self.pk})

    def get_create_voting_url(self):
        return reverse('create_voting', kwargs={'pk': self.pk})

    def get_republished_url(self):
        return reverse('republish_review', kwargs={'pk': self.pk})
