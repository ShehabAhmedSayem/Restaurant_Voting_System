from datetime import datetime
from rest_framework.test import APITransactionTestCase
from rest_framework import status
from django.urls import reverse
from voting.models import Result
from voting.tests.base_setup_model import SetUpModel


class ResultAPITest(APITransactionTestCase):
    """ Test module for API of the Result model. """

    def setUp(self):
        setUpObj = SetUpModel()
        self.admin = setUpObj.create_admin_type_user()
        self.owner = setUpObj.create_restaurant_owner_type_user()
        self.employee = setUpObj.create_employee_type_user()
        self.restaurant1 = setUpObj.create_restaurant(
                        owner=self.owner,
                        name='Restaurant 1'
                    )
        self.restaurant2 = setUpObj.create_restaurant(
                        owner=self.owner,
                        name='Restaurant 2'
                    )
        self.voting_date = datetime.now().date()
        self.menu = setUpObj.create_menu(
            restaurant=self.restaurant1,
            upload_date=self.voting_date
        )
        self.menu2 = setUpObj.create_menu(
            restaurant=self.restaurant2,
            upload_date=self.voting_date
        )
        self.result = setUpObj.create_result(self.voting_date)

    def publish_result_using_api(
        self, stop_voting=True, date=datetime.now().date()
    ):
        payload = {
            'stop_voting': stop_voting,
            'voting_date': date
        }
        return self.client.post(
            reverse('api:voting-api-v1:publish-result'),
            data=payload
        )

    # Tests regarding GET api
    def test_unauthenticated_user_can_not_get_result(self):
        response = self.client.get(
            reverse('api:voting-api-v1:result')
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_user_can_get_results(self):
        self.client.login(
            username=self.employee.username,
            password='password'
        )
        res = self.client.get(
            reverse('api:voting-api-v1:result')
        )
        self.client.logout()
        total_results = Result.objects.all().count()

        self.assertEqual(len(res.data), total_results)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Tests regarding POST api
    def test_restaurant_owner_can_not_publish_result(self):
        self.client.login(username=self.owner.username, password='password')
        res = self.publish_result_using_api(date=self.voting_date)
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_not_publish_result(self):
        self.client.login(
            username=self.employee.username,
            password='password'
        )
        res = self.publish_result_using_api(date=self.voting_date)
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_publish_result(self):
        self.client.login(username=self.admin.username, password='password')
        res = self.publish_result_using_api(date=self.voting_date)
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_not_publish_result_without_stopping_vote(self):
        self.client.login(username=self.admin.username, password='password')
        res = self.publish_result_using_api(False, date=self.voting_date)
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_publishing_result_increases_winning_streak_of_restaurant(self):
        self.restaurant1.refresh_from_db()
        previous_winning_streak = self.restaurant1.winning_streak
        self.client.login(
            username=self.admin.username,
            password='password'
        )
        res = self.publish_result_using_api(date=self.voting_date)
        self.client.logout()
        self.restaurant1.refresh_from_db()

        self.assertEqual(
            self.restaurant1.winning_streak, previous_winning_streak + 1
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_restaurant_with_3_consecutive_win_can_not_be_the_winner(self):
        self.client.login(
            username=self.admin.username,
            password='password'
        )
        self.restaurant1.winning_streak = 3
        self.restaurant1.save()
        res = self.publish_result_using_api(date=self.voting_date)
        self.client.logout()
        self.restaurant1.refresh_from_db()
        self.restaurant2.refresh_from_db()

        self.assertEqual(self.restaurant1.winning_streak, 0)
        self.assertEqual(self.restaurant2.winning_streak, 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
