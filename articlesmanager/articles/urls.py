from django.urls import path
from .views import (
    ArticlesList, ArticlesCreate, ArticlesUpdate, remove_author_from_article,
    select_author, add_author_to_article, ArticlesDetail, download_article, ArticlesDelete,
)


urlpatterns = [
    path('', ArticlesList.as_view(), name='articles'),
    path('create/', ArticlesCreate.as_view(), name='create_articles'),
    path('<int:pk>/detail/', ArticlesDetail.as_view(), name='detail_articles'),
    path('<int:pk>/download/', download_article, name='download_articles'),
    path('<int:pk>/delete/', ArticlesDelete.as_view(), name='delete_articles'),
    path('<int:pk>/update/', ArticlesUpdate.as_view(), name='update_articles'),
    path('<int:pk>/update/authors/', select_author, name='select_author'),
    path('<int:pk>/update/authors/<int:author_id>/remove/', remove_author_from_article, name='remove_author_from_article'),
    path('<int:pk>/update/authors/<int:author_id>/add/', add_author_to_article, name='add_author_to_article'),
]
