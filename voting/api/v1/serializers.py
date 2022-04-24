from rest_framework import serializers
from user.api.v1.serializers import UserSerializer
from voting.models import (
    Restaurant, Menu, Vote
)


class RestaurantSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'owner',
            'name',
            'address',
            'contact_no',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        return Restaurant.objects.create(
            **validated_data,
            owner=user
        )
