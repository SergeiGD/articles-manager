from django.core.exceptions import PermissionDenied


def check_is_reviewer(user, article):
    if user not in article.users.all():
        # проверяем, является ли юзер рецензентом
        raise PermissionDenied('Вы не являетесь рецензентом этой статьи')


def create_review(review, user, article):
    check_is_reviewer(user, article)
    # автоматически устанавливаем статью и юзера
    review.article = article
    review.user = user
    review.save()
