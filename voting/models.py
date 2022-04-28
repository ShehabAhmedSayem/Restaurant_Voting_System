from django.db import models
from django.core.exceptions import ValidationError
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
    winning_streak = models.PositiveIntegerField(
        verbose_name=_('Winning Streak'),
        default=0
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('Restaurant')
        verbose_name_plural = _('Restaurants')

    def __str__(self):
        return self.name

    def increment_winning_streak(self):
        self.winning_streak = models.F('winning_streak') + 1
        self.save()

    def reset_winning_streak(self):
        self.winning_streak = 0
        self.save()


def menu_image_upload_path(instance, filename):
    return f'menu/{instance.upload_date}/{instance.restaurant.name}/{filename}'


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
        verbose_name=_('Upload Date')
    )

    class Meta:
        ordering = ['-num_of_votes', 'id']
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

    def increment_num_of_votes(self):
        self.num_of_votes = models.F('num_of_votes') + 1
        self.save()

    def decrement_num_of_votes(self):
        self.num_of_votes = models.F('num_of_votes') - 1
        self.save()


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
        verbose_name=_('Voting Date')
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


class Result(ModelWithTimestamp):
    winning_menu = models.ForeignKey(
        verbose_name=_('Winning Menu'),
        to=Menu,
        related_name='results',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    voting_date = models.DateField(
        verbose_name=_('Voting Date'),
        unique=True
    )
    is_voting_stopped = models.BooleanField(
        verbose_name=_('Is Voting Stopped'),
        default=False
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def stop_voting(self):
        self.is_voting_stopped = True
        self.save()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.is_voting_stopped and self.winning_menu is None:
            raise ValidationError(
                {'winning_menu': _('Choose a winning menu.')}
            )

    def save(self, *args, **kwargs):
        if self.is_voting_stopped and self.winning_menu is None:
            raise ValidationError(
                message='Voting cannot be stopped without a winning menu.'
            )
        super(Result, self).save(*args, **kwargs)
