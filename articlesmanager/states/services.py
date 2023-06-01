from django.utils import timezone


def delete_state(state):
    state.date_deleted = timezone.now()
    state.save()