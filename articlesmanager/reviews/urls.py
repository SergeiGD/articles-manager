from django.urls import path
from .views import ReviewsList


urlpatterns = [
    path('', ReviewsList.as_view(), name='reviews'),
    path('create/', ReviewsList.as_view(), name='reviews'),

]
