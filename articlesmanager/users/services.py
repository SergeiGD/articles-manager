from django.core.mail import EmailMessage
from django.utils import timezone

from .models import CustomUser


def register_user(user):
    # автоматически генериуем пароль
    password = CustomUser.objects.make_random_password()
    user.set_password(password)
    user.save()
    # отправляем пароль на почту
    email = EmailMessage(
        subject='Регистрация',
        body=f'Ваш аккаунт создан. Пароль - {password}',
        to=[user.email, ],
    )
    email.send()


def delete_user(user):
    # т.к. реально не удаляем и email является уникальным, изменим email, чтоб освободить его
    email = f'{user.email}_deleted'
    count = 1
    while CustomUser.objects.filter(email=email).exists():
        email = f'{email}_deleted_{count}'
        # просто прибавляем счетчик на 1, пока не станет свободна почта (если удаляли несколько раз)
        count += 1
    user.date_deleted = timezone.now()
    user.email = email
    user.save()


def reset_user(user):
    password = CustomUser.objects.make_random_password()
    user.set_password(password)
    user.save()
    # отправляем пароль на почту
    email = EmailMessage(
        subject='Изменение пароля',
        body=f'Ваш пароль был изменен на {password}',
        to=[user.email, ],
    )
    email.send()


def delete_position(position):
    position.date_deleted = timezone.now()
    position.save()


def get_articles_to_review(user):
    """
    Получение списка стетей для ревью
    """
    result = []
    # статьи, где юзер ревьювер
    user_articles = user.articles.filter(
        date_deleted=None,
        users__in=[user],
        voting__isnull=True,
    ).all()
    for article in user_articles:
        if not article.reviews.filter(
                user=user,
                date_created__gt=article.date_repulished,
        ).exists():
            # если не делал ревью на статью после внесения правок
            result.append(article)

    return user.articles.filter(id__in=[i.id for i in result])


def can_create_review(user, article):
    # проверка, может ли юзер создать ревью
    if article.date_deleted is not None or article.votings.exists():
        # если статья удалена или уже проводится голосование
        return False

    if user not in article.users.all():
        # если не является ревьювером
        return False

    if article.reviews.filter(
        user=user,
        date_created__gt=article.date_repulished
    ).exists():
        # если уже есть ревью и в статью при этом не вносились правки
        return False

    return True
