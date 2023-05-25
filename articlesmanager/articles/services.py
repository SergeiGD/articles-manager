from django.utils import timezone

from articles.models import ArticleState
from notifications.services import create_republished_notification


def save_article(article, state):
    if article.get_current_state() != state:
        # устанавливаем статус и время присвоения
        ArticleState.objects.update_or_create(
            state_id=state.id,
            article_id=article.id,
            date_set=timezone.now()
        )


def republish_article(user, article):
    # устанавливаем время
    article.date_repulished = timezone.now()
    article.save()
    create_republished_notification(article)


def delete_article(article):
    article.date_deleted = timezone.now()
    article.save()


def is_enable_for_voting(article):
    """
    Проверка, можно ли создать голосование
    """
    if article.votings.exists():
        # если голосование уже существует, то нельзя
        return False

    if article.reviews.filter(
            date_created__gt=article.date_repulished,
    ).count() < article.users.filter(date_deleted=None).count():
        # если не все сделали рецензию
        return False

    if article.count_approved <= article.count_unapproved:
        # если отрицательных рецензий больше
        return False

    return True
