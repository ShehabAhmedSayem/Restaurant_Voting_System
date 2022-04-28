from datetime import datetime
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from voting.tests.base_setup_model import SetUpModel


class MenuModelTests(TestCase):

    def test_restaurant_can_upload_only_one_menu_per_day(self):
        """
        Testing restaurant and upload_day unique constraints of Menu Model.
        """

        setUp = SetUpModel()
        owner = setUp.create_restaurant_owner_type_user()
        restaurant = setUp.create_restaurant(owner=owner)
        upload_date = datetime.now().date()
        setUp.create_menu(restaurant, upload_date)
        self.assertRaises(
            IntegrityError, lambda: (
                setUp.create_menu(restaurant, upload_date)
            )
        )


class VoteModelTests(TestCase):

    def test_employee_can_vote_only_once_per_day(self):
        """
        Testing employee and voting_day unique constraints of Menu Model.
        """

        setUp = SetUpModel()
        employee = setUp.create_employee_type_user()
        owner = setUp.create_restaurant_owner_type_user()
        restaurant = setUp.create_restaurant(owner=owner)
        upload_date = datetime.now().date()
        menu = setUp.create_menu(restaurant, upload_date)
        setUp.create_vote(employee, menu, voting_date=upload_date)
        self.assertRaises(
            IntegrityError, lambda: (
                setUp.create_vote(employee, menu, voting_date=upload_date)
            )
        )


class ResultModelTests(TestCase):

    def test_voting_cannot_be_stopped_without_choosing_winning_menu(self):
        """
        Testing winning_menu is not null if voting is stopped of Result model.
        """

        upload_date = datetime.now().date()
        setUp = SetUpModel()
        result = setUp.create_result(upload_date)
        self.assertRaises(
            ValidationError, lambda: (
                result.stop_voting()
            )
        )
