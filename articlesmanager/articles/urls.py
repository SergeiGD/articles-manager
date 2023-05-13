from django.urls import path
from .views import (
    ArticlesList, ArticlesCreate, ArticlesUpdate, remove_author_from_article,
    SelectAuthorsList, add_author_to_article, ArticlesDetail, download_article, ArticlesDelete,
    add_user_to_article, remove_user_from_article, SelectUsersList,
    mark_as_republished
)
from reviews.views import ReviewsCreate, ReviewDetail
from votings.views import VotingsCreate


urlpatterns = [
    path('', ArticlesList.as_view(), name='articles'),
    path('create/', ArticlesCreate.as_view(), name='create_articles'),
    path('<int:pk>/republish/', mark_as_republished, name='republish_review'),
    path('<int:pk>/review/', ReviewsCreate.as_view(), name='create_review'),
    path('<int:pk>/review/<int:review_id>', ReviewDetail.as_view(), name='detail_review'),
    path('<int:pk>/voting/', VotingsCreate.as_view(), name='create_voting'),
    path('<int:pk>/detail/', ArticlesDetail.as_view(), name='detail_articles'),
    path('<int:pk>/download/', download_article, name='download_articles'),
    path('<int:pk>/delete/', ArticlesDelete.as_view(), name='delete_articles'),
    path('<int:pk>/update/', ArticlesUpdate.as_view(), name='update_articles'),
    path('<int:pk>/update/authors/', SelectAuthorsList.as_view(), name='select_author'),
    path('<int:pk>/update/authors/<int:author_id>/remove/', remove_author_from_article, name='remove_author_from_article'),
    path('<int:pk>/update/authors/<int:author_id>/add/', add_author_to_article, name='add_author_to_article'),
    path('<int:pk>/update/users/', SelectUsersList.as_view(), name='select_user_for_article'),
    path('<int:pk>/update/users/<int:user_id>/remove/', remove_user_from_article, name='remove_user_from_article'),
    path('<int:pk>/update/users/<int:user_id>/add/', add_user_to_article, name='add_user_to_article'),
]
