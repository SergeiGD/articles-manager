from django.urls import path
from .views import CustomLoginView, logout_view, Index


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', Index.as_view(), name='index'),
]
