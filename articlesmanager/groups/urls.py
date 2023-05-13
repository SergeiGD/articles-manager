from django.urls import path
from .views import (
    GroupsCreate, GroupsList, GroupsUpdate, GroupsDetail, GroupsDelete,
    SelectPermissionsList, add_permission_to_group, remove_permission_from_group,
    SelectUsersList, add_user_to_group, remove_user_from_group,
)


urlpatterns = [
    path('', GroupsList.as_view(), name='groups'),
    path('create/', GroupsCreate.as_view(), name='create_groups'),
    path('<int:pk>/update/', GroupsUpdate.as_view(), name='update_groups'),
    path('<int:pk>/detail/', GroupsDetail.as_view(), name='detail_groups'),
    path('<int:pk>/delete/', GroupsDelete.as_view(), name='delete_groups'),
    path('<int:pk>/update/permissions/', SelectPermissionsList.as_view(), name='select_permission'),
    path('<int:pk>/update/permissions/<int:permission_id>/add/', add_permission_to_group, name='add_permission_to_group'),
    path('<int:pk>/update/permissions/<int:permission_id>/remove/', remove_permission_from_group, name='remove_permission_from_group'),
    path('<int:pk>/update/users/', SelectUsersList.as_view(), name='select_user_for_group'),
    path('<int:pk>/update/users/<int:user_id>/add/', add_user_to_group, name='add_user_to_group'),
    path('<int:pk>/update/users/<int:user_id>/remove/', remove_user_from_group, name='remove_user_from_group'),
]
