from django.urls import path
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView
)
from user.api.v1.views import RegisterView, UserDetailsView


app_name = 'user-api-v1'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('profile/', UserDetailsView.as_view(), name='profile'),
    path(
        'password/change/',
        PasswordChangeView.as_view(),
        name='rest_password_change'
    ),
]
