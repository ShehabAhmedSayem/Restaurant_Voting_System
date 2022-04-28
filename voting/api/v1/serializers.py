from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError
from user.api.v1.serializers import UserSerializer
from voting.models import (
    Restaurant, Menu, Result, Vote
)


class RestaurantSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    winning_streak = serializers.ReadOnlyField()

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'owner',
            'name',
            'address',
            'contact_no',
            'winning_streak'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        return Restaurant.objects.create(
            **validated_data,
            owner=user
        )


class MenuSerializer(serializers.ModelSerializer):
    num_of_votes = serializers.ReadOnlyField()

    class Meta:
        model = Menu
        fields = [
            'id',
            'restaurant',
            'menu_image',
            'num_of_votes',
            'upload_date',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['restaurant'] = RestaurantSerializer(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        restaurant = validated_data.get('restaurant')
        if restaurant.owner != user:
            raise PermissionDenied(
                detail='You are not the owner of this restaurant.'
            )
        try:
            return Menu.objects.create(
                **validated_data,
            )
        except IntegrityError:
            raise ValidationError(detail=(
                "You have already uploaded today's menu for this restaurant."
                )
            )

    def update(self, instance, validated_data):
        upload_date = validated_data.get('upload_date', None)
        if upload_date:
            validated_data.pop('upload_date')
            if upload_date != instance.upload_date:
                raise serializers.ValidationError(
                    'You cannot change the upload date of the menu.'
                )
        return super().update(instance, validated_data)


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = [
            'id',
            'menu',
            'voting_date',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['menu'] = MenuSerializer(
                read_only=True, context={'request': self.context['request']}
            )

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            result, _ = Result.objects.get_or_create(
                            voting_date=validated_data['voting_date']
                        )
            if result.is_voting_stopped:
                raise PermissionDenied(
                    detail="Sorry! Voting is stopped for today."
                )
            if (
                validated_data['voting_date']
                != validated_data['menu'].upload_date
            ):
                raise ValidationError(
                    detail="Voting date and menu upload date must be same."
                )
            return Vote.objects.create(
                **validated_data,
                employee=user
            )
        except IntegrityError:
            raise ValidationError(detail='You have already voted.')

    def update(self, instance, validated_data):
        voting_date = validated_data.get('voting_date', None)
        if voting_date:
            validated_data.pop('voting_date')
            if voting_date != instance.voting_date:
                raise serializers.ValidationError(
                    'You cannot change the voting date.'
                )
        return super().update(instance, validated_data)


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = [
            'id',
            'winning_menu',
            'voting_date',
            'is_voting_stopped'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['winning_menu'] = MenuSerializer(
                context={'request': self.context['request']}
            )


class PublishResultSerializer(serializers.Serializer):
    stop_voting = serializers.BooleanField(required=True)
    voting_date = serializers.DateField(required=True)
