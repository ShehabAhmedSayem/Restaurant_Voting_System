from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


def expires_in(token):
    """
    Returns the time left of a token.
    """
    time_elapsed = timezone.now() - token.created
    left_time = (
        timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    )
    return left_time


def is_token_expired(token):
    """
    Returns if token expired or not.
    """
    return expires_in(token) < timedelta(seconds=0)


def token_expire_handler(token):
    """
    Returns if token is expired or not
    and the current token or the newly created token.
    """
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token


# DEFAULT_AUTHENTICATION_CLASSES
class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed(_('The Token is expired'))

        return (token.user, token)
