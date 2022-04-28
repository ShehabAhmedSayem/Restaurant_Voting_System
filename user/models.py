from django.db import models
from django.contrib.auth.models import AbstractUser as BaseUser
from django.utils.translation import gettext_lazy as _


class CustomUser(BaseUser):
    class UserType(models.IntegerChoices):
        ADMIN = 1, _('Admin')
        EMPLOYEE = 2, _('Employee')
        RESTAURANT_OWNER = 3, _('Restaurant_owner')

    user_type = models.SmallIntegerField(
        verbose_name=_('User Type'),
        choices=UserType.choices,
        default=UserType.ADMIN
    )

    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['id']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username
