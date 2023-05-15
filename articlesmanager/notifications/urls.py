from django.urls import path
from .views import NotificationsList, NotificationsDetail, mark_as_checked, NotificationsDelete


urlpatterns = [
    path('', NotificationsList.as_view(), name='notifications'),
    path('<int:pk>/', NotificationsDetail.as_view(), name='detail_notifications'),
    path('<int:pk>/checked/', mark_as_checked, name='mark_as_checked'),
    path('<int:pk>/delete/', NotificationsDelete.as_view(), name='delete_notifications'),
]
