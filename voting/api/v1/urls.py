from django.urls import path
from voting.api.v1.views import (
    RestaurantListCreateAPIView, RestaurantRUDAPIView,
    MenuListCreateAPIView, MenuRUDAPIView, VoteListCreateAPIView,
    VoteRUDAPIView, ResultAPIView, PublishResultAPIView
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
    path('menus/', MenuListCreateAPIView.as_view(), name='menu-list-create'),
    path('menus/<int:pk>/', MenuRUDAPIView.as_view(), name='menu-rud'),
    path('votes/', VoteListCreateAPIView.as_view(), name='vote-list-create'),
    path('votes/<int:pk>/', VoteRUDAPIView.as_view(), name='vote-rud'),
    path('result/', ResultAPIView.as_view(), name='result'),
    path(
        'publish-result/',
        PublishResultAPIView.as_view(),
        name='publish-result'
    ),
]
