from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import ModelWithTimestamp
from user.models import CustomUser


class Restaurant(ModelWithTimestamp):
    owner = models.ForeignKey(
        verbose_name=_('Owner'),
        to=CustomUser,
        related_name='restaurants',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=128
    )
    address = models.TextField(
        verbose_name=_('Address'),
        blank=True,
        default=""
    )
    contact_no = models.CharField(
        verbose_name=_('Contact No'),
        max_length=24,
        blank=True,
        default=""
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('Restaurant')
        verbose_name_plural = _('Restaurants')

    def __str__(self):
        return self.name


def menu_image_upload_path(instance, filename):
    return f'menus/{instance.restaurant.name}/{filename}'


class Menu(ModelWithTimestamp):
    restaurant = models.ForeignKey(
        verbose_name=_('Restaurant'),
        to=Restaurant,
        related_name='menus',
        on_delete=models.CASCADE
    )
    menu_image = models.ImageField(
        verbose_name=_('Menu Image'),
        upload_to=menu_image_upload_path,
        max_length=255
    )
    num_of_votes = models.PositiveIntegerField(
        verbose_name=_('Number of Votes'),
        default=0
    )
    upload_date = models.DateField(
        verbose_name=_('Upload Date'),
        auto_now_add=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
        constraints = [
            models.UniqueConstraint(
                fields=['restaurant', 'upload_date'],
                name='unique_restaurant_menu_per_day'
            )
        ]

    def __str__(self):
        return f'{self.restaurant}_{self.id}'


class Vote(ModelWithTimestamp):
    employee = models.ForeignKey(
        verbose_name=_('Employee'),
        to=CustomUser,
        related_name='votes',
        on_delete=models.CASCADE
    )
    menu = models.ForeignKey(
        verbose_name=_('Menu'),
        to=Menu,
        related_name='votes',
        on_delete=models.CASCADE
    )
    voting_date = models.DateField(
        verbose_name=_('Voting Date'),
        auto_now_add=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'voting_date'],
                name='unique_employee_vote_per_day'
            )
        ]
