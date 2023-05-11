from django.urls import path
from .views import UsersList, UsersCreate


urlpatterns = [
    path('', UsersList.as_view(), name='users'),
    path('create/', UsersCreate.as_view(), name='create_users')
]