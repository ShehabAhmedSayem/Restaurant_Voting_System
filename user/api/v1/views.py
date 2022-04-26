from dj_rest_auth.registration.views import RegisterView as DJRegisterView
from user.api.v1.serializers import UserSerializer


class RegisterView(DJRegisterView):

    def get_response_data(self, user):
        return UserSerializer(user).data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user
