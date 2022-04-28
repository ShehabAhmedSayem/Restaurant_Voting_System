from dj_rest_auth.registration.views import RegisterView as DJRegisterView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from user.api.v1.serializers import UserSerializer


class RegisterView(DJRegisterView):

    def get_response_data(self, user):
        return UserSerializer(user).data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user


class UserDetailsView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
