def delete_state(state):
    state.date_deleted = timezone.now()
    state.save()