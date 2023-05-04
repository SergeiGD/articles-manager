from django.urls import path
from .views import AuthorsCreate, AuthorsList, AuthorsUpdate, AuthorsDetail, delete_author, AuthorsDelete


urlpatterns = [
    path('', AuthorsList.as_view(), name='authors'),
    path('create/', AuthorsCreate.as_view(), name='create_authors'),
    path('<int:pk>/update/', AuthorsUpdate.as_view(), name='update_authors'),
    path('<int:pk>/detail/', AuthorsDetail.as_view(), name='detail_authors'),
    # path('<int:pk>/delete/', delete_author, name='delete_authors'),
    path('<int:pk>/delete/', AuthorsDelete.as_view(), name='delete_authors'),
]
