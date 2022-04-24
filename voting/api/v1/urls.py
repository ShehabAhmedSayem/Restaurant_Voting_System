from django.urls import path
from voting.api.v1.views import (
    RestaurantListCreateAPIView, RestaurantRUDAPIView
)


app_name = 'voting-api-v1'

urlpatterns = [
    path(
        'restaurants/',
        RestaurantListCreateAPIView.as_view(),
        name='restaurant-list-create'
    ),
    path(
        'restaurants/<int:pk>/',
        RestaurantRUDAPIView.as_view(),
        name='restaurant-rud'
    ),
]
