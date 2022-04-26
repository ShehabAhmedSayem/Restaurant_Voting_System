from rest_framework import permissions
from user.models import CustomUser


class IsSecretKeyValid(permissions.BasePermission):
    """
    Allows access only to accurate secret key.
    """

    def has_permission(self, request, view):
        secret = request.headers.get('Api-Secret')
        return bool(secret and secret == 'nd2s1h@eReT#yU3j')


class IsUserAdmin(permissions.BasePermission):
    """
    Allow access only if the user_type is admin.
    """

    message = 'Not an admin.'

    def has_permission(self, request, view):
        return request.user.user_type == CustomUser.UserType.ADMIN


class IsUserEmployee(permissions.BasePermission):
    """
    Allow access only if the user_type is employee.
    """

    message = 'Not an employee.'

    def has_permission(self, request, view):
        return request.user.user_type == CustomUser.UserType.EMPLOYEE


class IsUserRestaurantOwner(permissions.BasePermission):
    """
    Allow access only if the user_type is restaurant_owner.
    """

    message = 'Not a restaurant owner.'

    def has_permission(self, request, view):
        return request.user.user_type == CustomUser.UserType.RESTAURANT_OWNER


class IsUserOwnsRestaurant(permissions.BasePermission):
    """
    Allow object edit access only if the user is the owner of the restaurant.
    """

    message = 'Not the owner of the restaurant.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsUserOwnsMenu(permissions.BasePermission):
    """
    Allow object edit access only if the user is the owner of the menu.
    """

    message = 'Not the owner of the restaturant of the menu.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.restaurant.owner
