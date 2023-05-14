from django.urls import path
from .views import NotificationsList


urlpatterns = [
    path('', NotificationsList.as_view(), name='notifications'),
]
