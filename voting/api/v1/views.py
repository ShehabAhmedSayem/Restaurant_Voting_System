from django.http import Http404
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView, get_object_or_404
)
from rest_framework.permissions import IsAuthenticated
from core.api.permissions import (
    IsUserAdmin, IsUserEmployee, IsUserRestaurantOwner, IsUserOwnsRestaurant
)
from voting.models import Restaurant
from voting.api.v1.serializers import RestaurantSerializer


class RestaurantListCreateAPIView(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsUserRestaurantOwner]

    def get_permissions(self):
        if self.request.method == 'GET':
            """ Any authenticated user can see the restaurant list """
            return [IsAuthenticated()]
        return super().get_permissions()


class RestaurantRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsUserOwnsRestaurant]

    def get_permissions(self):
        if self.request.method == 'GET':
            """ Any authenticated user can see the restaurant details. """
            return [IsAuthenticated()]
        return super().get_permissions()
