from django.urls import path
from .views import ReviewsList, ReviewUpdate


urlpatterns = [
    path('', ReviewsList.as_view(), name='reviews'),
    path('<int:pk>/update/', ReviewUpdate.as_view(), name='update_review'),

]
