from django.urls import path
from .views import (
    UsersList, UsersCreate, UsersDetail, UsersUpdate, UsersDelete, reset_user_password,
    add_group_to_user, remove_group_from_user, SelectGroupsList
)


urlpatterns = [
    path('', UsersList.as_view(), name='users'),
    path('create/', UsersCreate.as_view(), name='create_users'),
    path('<int:pk>/detail/', UsersDetail.as_view(), name='detail_users'),
    path('<int:pk>/update/', UsersUpdate.as_view(), name='update_users'),
    path('<int:pk>/delete/', UsersDelete.as_view(), name='delete_users'),
    path('<int:pk>/reset/', reset_user_password, name='reset_user_password'),
    path('<int:pk>/update/groups/', SelectGroupsList.as_view(), name='select_group_for_user'),
    path('<int:pk>/update/groups/<int:group_id>/add/', add_group_to_user, name='add_group_to_user'),
    path('<int:pk>/update/groups/<int:group_id>/remove/', remove_group_from_user, name='remove_group_from_user'),
]