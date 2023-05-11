from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils import timezone
from authors.models import Author
from states.models import State
from users.models import CustomUser


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
    file = models.FileField(verbose_name='Файл')
    unique = models.FloatField(verbose_name='Оригинальность')
    bibliography = models.TextField(verbose_name='Библиография')
    quoting = models.FloatField(verbose_name='Степень цитирования')
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


    def get_current_state(self):
        return self.states.filter(
            articlestate__date_set=self.states.aggregate(max_date=Max('articlestate__date_set'))['max_date']
        ).first()

    def save(self, *args, **kwargs):
        self.date_edited = timezone.now()
        super().save(*args, **kwargs)

    def get_update_url(self):
        return reverse('update_articles', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_articles', kwargs={'pk': self.pk})

    def get_show_url(self):
        return reverse('detail_articles', kwargs={'pk': self.pk})

    def get_download_url(self):
        return reverse('download_articles', kwargs={'pk': self.pk})

    def get_select_author_url(self):
        return reverse('select_author', kwargs={'pk': self.pk})

    def get_select_user_url(self):
        return reverse('select_user', kwargs={'pk': self.pk})
