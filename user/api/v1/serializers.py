from rest_framework import serializers
from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "user_type",
            "username",
            "first_name",
            "first_name",
            "email",
        ]
