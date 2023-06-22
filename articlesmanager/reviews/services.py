from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect


def check_is_reviewer(user, article):
    if user not in article.users.all():
        # проверяем, является ли юзер рецензентом
        raise PermissionDenied('Вы не являетесь рецензентом этой статьи')


def check_is_already_reviewed(user, article):
    if article.reviews.filter(
        user=user,
        date_created__gte=article.date_repulished
    ).exists():
        return True
    return False


def create_review(review, user, article):
    check_is_reviewer(user, article)
    if check_is_already_reviewed(user, article):
        return HttpResponseRedirect(article.get_detail_url())
    # автоматически устанавливаем статью и юзера
    review.article = article
    review.user = user
    review.save()
