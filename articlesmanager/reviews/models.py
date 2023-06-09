from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import CustomUser
from articles.models import Article


class Review(models.Model):
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    approved = models.BooleanField(verbose_name='Одобрено', default=False)
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT,
        verbose_name='Проверяющий',
        related_name='reviews',
        related_query_name='reviewss',
    )
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        verbose_name='Статья',
        related_name='reviews',
        related_query_name='review',
    )
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def get_detail_url(self):
        return reverse('detail_review', kwargs={'review_id': self.pk, 'pk': self.article.pk})

    def get_update_url(self):
        return reverse('update_review', kwargs={'pk': self.pk })