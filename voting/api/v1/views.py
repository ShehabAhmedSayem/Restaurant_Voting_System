from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.api.permissions import (
    IsUserAdmin, IsUserEmployee, IsUserRestaurantOwner,
    IsUserOwnsRestaurant, IsUserOwnsMenu
)
from voting.models import (
    Restaurant, Menu, Vote, Result
)
from voting.api.v1.serializers import (
    RestaurantSerializer, MenuSerializer, VoteSerializer,
    ResultSerializer, PublishResultSerializer
)
from voting.utils import update_result


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


class MenuListCreateAPIView(ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant', 'upload_date']
    permission_classes = [IsAuthenticated, IsUserRestaurantOwner]

    def get_permissions(self):
        if self.request.method == 'GET':
            """ Any authenticated user can see the menu list """
            return [IsAuthenticated()]
        return super().get_permissions()


class MenuRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsUserOwnsMenu]

    def get_permissions(self):
        if self.request.method == 'GET':
            """ Any authenticated user can see the menu details. """
            return [IsAuthenticated()]
        return super().get_permissions()


class VoteListCreateAPIView(ListCreateAPIView):
    serializer_class = VoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['voting_date']
    permission_classes = [IsAuthenticated, IsUserEmployee]

    def get_queryset(self):
        return Vote.objects.filter(employee=self.request.user)


class VoteRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated, IsUserEmployee]

    def get_queryset(self):
        return Vote.objects.filter(employee=self.request.user)


class ResultAPIView(ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['voting_date']
    permission_classes = [IsAuthenticated]


class PublishResultAPIView(APIView):
    serializer_class = PublishResultSerializer
    permission_classes = [IsAuthenticated, IsUserAdmin]

    def post(self, request, format=None):
        serializer = PublishResultSerializer(data=request.data)
        json_res = {}
        status_code = status.HTTP_200_OK
        if serializer.is_valid():
            stop_voting = serializer.validated_data['stop_voting']
            voting_date = serializer.validated_data['voting_date']
            if stop_voting:
                success, result = update_result(voting_date)
                if success:
                    json_res = {
                        'message': 'Success!',
                        'winner': MenuSerializer(
                                    result.winning_menu,
                                    context={'request': self.request}
                                ).data
                    }
                else:
                    json_res = {
                        'message': 'No menu found for today. So no winner!',
                        'winner': None
                    }
                    status_code = status.HTTP_204_NO_CONTENT
            else:
                json_res = {
                    'message': 'Voting must be stopped to get result!',
                    'winner': None
                }
        else:
            json_res = {
                'message': 'Invalid data'
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(json_res, status_code)
