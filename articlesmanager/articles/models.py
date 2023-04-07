from django.db import models
from django.utils import timezone
from authors.models import Author
from states.models import State


class ArticleState(models.Model):
    article = models.ForeignKey(
        to='Article',
        on_delete=models.CASCADE,
    )
    state = models.ForeignKey(
        to=State,
        on_delete=models.CASCADE,
    )
    date_set = models.DateTimeField(default=timezone.now, verbose_name='Дата присвоения')



class Article(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    file = models.FileField(verbose_name='Файл')
    unique = models.FloatField(verbose_name='Оригинальность')
    bibliography = models.TextField(verbose_name='Библиография')
    quoting = models.TextField(verbose_name='Степень цитирования')
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
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')


