from django.utils import timezone
from .models import VotingUsers


def change_vote(vote, agreed):
    """
    Изменение голоса
    """
    vote.agreed = agreed
    vote.date_changed = timezone.now()
    vote.save()


def create_vote(voting, user, agreed):
    """
    Создание голоса
    """
    VotingUsers.objects.create(
        voting_id=voting.id,
        user_id=user.id,
        agreed=agreed,
        date_changed=timezone.now(),
    )


def get_current_vote(vote):
    """
    Получение текущаего голоса
    """
    if vote is not None:
        if vote.agreed:
            return 'За'
        else:
            return 'Против'
    else:
        return 'Нет голоса'


def is_enable_to_vote(vote):
    """
    Доступна ли для голосования
    """
    return vote.date_start < timezone.now() < vote.date_end
