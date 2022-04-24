from rest_framework import permissions


class IsSecretKeyValid(permissions.BasePermission):
    """
    Allows access only to accurate mobile secret.
    """

    def has_permission(self, request, view):
        secret = request.headers.get('Api-Secret')
        return bool(secret and secret == 'nd2s1h@eReT#yU3j')
