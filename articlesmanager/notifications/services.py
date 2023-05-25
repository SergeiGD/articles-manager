from .models import Notification


def create_reviewer_notification(user, article):
    Notification.objects.create(
        user=user,
        subject=Notification.NotificationsSubjects.REVIEWER,
        content=f'Вас назначили рецензентом на статью <a href="{article.get_detail_url()}">{article.name}</a>',
        article=article,
    )

def create_republished_notification(user, article):
    Notification.objects.create(
        user=user,
        subject=Notification.NotificationsSubjects.ARTICLE_REPUBLISHED,
        content=f'В статью <a href="{article.get_detail_url()}">{article.name}</a> внесены правки, требуется рецензия',
        article=article,
    )

def create_voting_notification(voting, user, article):
    Notification.objects.create(
            user=user,
            subject=Notification.NotificationsSubjects.VOTING,
            content=f'Назначено голосование <a href="{voting.get_detail_url()}">{voting.article.name}</a>. Дата начала - {voting.date_start}',
            article=article,
        )
