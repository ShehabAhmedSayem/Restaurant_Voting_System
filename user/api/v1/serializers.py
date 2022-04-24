from rest_framework import serializers
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DJRegisterSerializer
)
from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "user_type",
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class RegisterSerializer(DJRegisterSerializer):
    user_type = serializers.ChoiceField(choices=CustomUser.UserType)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'user_type': self.validated_data.get('user_type', ''),
        }
