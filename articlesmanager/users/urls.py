from django.urls import path
from .views import UsersList, UsersCreate, UsersDetail, UsersUpdate, UsersDelete, reset_user_password


urlpatterns = [
    path('', UsersList.as_view(), name='users'),
    path('create/', UsersCreate.as_view(), name='create_users'),
    path('<int:pk>/detail/', UsersDetail.as_view(), name='detail_users'),
    path('<int:pk>/update/', UsersUpdate.as_view(), name='update_users'),
    path('<int:pk>/delete/', UsersDelete.as_view(), name='delete_users'),
    path('<int:pk>/reset/', reset_user_password, name='reset_user_password'),
]