from django.urls import path
from .views import StatesCreate, StatesList, StatesUpdate, StatesDetail, StatesDelete


urlpatterns = [
    path('', StatesList.as_view(), name='states'),
    path('create/', StatesCreate.as_view(), name='create_states'),
    path('<int:pk>/update/', StatesUpdate.as_view(), name='update_states'),
    path('<int:pk>/detail/', StatesDetail.as_view(), name='detail_states'),
    path('<int:pk>/delete/', StatesDelete.as_view(), name='delete_states'),
]
