from django.urls import path
from .views import VotingsList, VotingsUpdate, VotingsDetail, VotingsDelete, voting_agreed, voting_disagreed


urlpatterns = [
    path('', VotingsList.as_view(), name='votings'),
    path('<int:pk>/update/', VotingsUpdate.as_view(), name='votings_update'),
    path('<int:pk>/detail/', VotingsDetail.as_view(), name='votings_detail'),
    path('<int:pk>/delete/', VotingsDelete.as_view(), name='votings_delete'),
    path('<int:pk>/agreed/', voting_agreed, name='votings_agreed'),
    path('<int:pk>/disagreed/', voting_disagreed, name='votings_disagreed'),
]
