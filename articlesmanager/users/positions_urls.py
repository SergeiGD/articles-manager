from django.urls import path
from .views import PositionsCreate, PositionsList, PositionsUpdate, PositionsDelete, PositionsDetail


urlpatterns = [
    path('', PositionsList.as_view(), name='positions'),
    path('create/', PositionsCreate.as_view(), name='create_positions'),
    path('<int:pk>/update/', PositionsUpdate.as_view(), name='update_positions'),
    path('<int:pk>/detail/', PositionsDetail.as_view(), name='detail_positions'),
    path('<int:pk>/delete/', PositionsDelete.as_view(), name='delete_positions'),
]
