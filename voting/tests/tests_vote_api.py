from datetime import datetime, timedelta
from rest_framework.test import APITransactionTestCase
from rest_framework import status
from django.urls import reverse
from voting.models import Vote
from voting.tests.base_setup_model import SetUpModel


class VoteListCreateAPITest(APITransactionTestCase):
    """ Test module for list create API of the Vote model. """

    def setUp(self):
        setUpObj = SetUpModel()
        self.admin = setUpObj.create_admin_type_user()
        self.owner = setUpObj.create_restaurant_owner_type_user()
        self.employee1 = setUpObj.create_employee_type_user()
        self.employee2 = setUpObj.create_employee_type_user(username='emp2')
        self.employee3 = setUpObj.create_employee_type_user(username='emp3')
        self.restaurant1 = setUpObj.create_restaurant(
                        owner=self.owner,
                        name='Restaurant 1'
                    )
        self.restaurant2 = setUpObj.create_restaurant(
                        owner=self.owner,
                        name='Restaurant 2'
                    )
        self.voting_date = datetime.now().date()
        self.menu1 = setUpObj.create_menu(
            restaurant=self.restaurant1,
            upload_date=self.voting_date
        )
        self.menu2 = setUpObj.create_menu(
            restaurant=self.restaurant2,
            upload_date=self.voting_date
        )
        self.vote1 = setUpObj.create_vote(
            employee=self.employee1,
            menu=self.menu1,
            voting_date=self.voting_date
        )
        self.vote2 = setUpObj.create_vote(
            employee=self.employee2,
            menu=self.menu2,
            voting_date=self.voting_date
        )
        self.result = setUpObj.create_result(self.voting_date)

    def create_vote_using_api(self, menu, date=datetime.now().date()):
        payload = {
            'menu': menu.pk,
            'voting_date': date
        }
        return self.client.post(
            reverse('api:voting-api-v1:vote-list-create'),
            data=payload
        )

    # Tests regarding GET api
    def test_only_authenticated_user_can_get_votes(self):
        response = self.client.get(
            reverse('api:voting-api-v1:vote-list-create')
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_employee_user_can_get_his_votes(self):
        self.client.login(
            username=self.employee1.username,
            password='password'
        )
        res = self.client.get(
            reverse('api:voting-api-v1:vote-list-create')
        )
        self.client.logout()
        total_votes = Vote.objects.filter(employee=self.employee1).count()
        self.assertEqual(len(res.data), total_votes)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Tests regarding POST api
    def test_admin_can_not_vote(self):
        self.client.login(username=self.admin.username, password='password')
        res = self.create_vote_using_api(menu=self.menu1)
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_owner_can_not_vote(self):
        self.client.login(username=self.owner.username, password='password')
        res = self.create_vote_using_api(menu=self.menu1)
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_not_vote_after_voting_is_stopped(self):
        self.client.login(
            username=self.employee3.username,
            password='password'
        )
        self.result.winning_menu = self.menu1
        self.result.stop_voting()
        res = self.create_vote_using_api(menu=self.menu2)
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_vote(self):
        self.client.login(
            username=self.employee3.username,
            password='password'
        )
        res = self.create_vote_using_api(menu=self.menu2)
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_creating_vote_increases_num_of_votes_of_menu(self):
        self.menu2.refresh_from_db()
        previous_num_of_votes = self.menu2.num_of_votes
        self.client.login(
            username=self.employee3.username,
            password='password'
        )
        res = self.create_vote_using_api(menu=self.menu2)
        self.client.logout()
        self.menu2.refresh_from_db()

        self.assertEqual(self.menu2.num_of_votes, previous_num_of_votes + 1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_employee_can_vote_once_per_day(self):
        self.client.login(
            username=self.employee3.username,
            password='password'
        )
        res1 = self.create_vote_using_api(menu=self.menu1)
        res2 = self.create_vote_using_api(menu=self.menu2)
        self.client.logout()

        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_can_not_vote_menu_of_another_day(self):
        self.client.login(
            username=self.employee1.username,
            password='password'
        )
        res = self.create_vote_using_api(
                menu=self.menu2,
                date=self.voting_date + timedelta(days=1)
            )
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class VoteRUDAPITest(APITransactionTestCase):
    """ Test module for RUD API of the menu model. """

    def setUp(self):
        setUpObj = SetUpModel()
        self.admin = setUpObj.create_admin_type_user()
        self.owner = setUpObj.create_restaurant_owner_type_user()
        self.employee1 = setUpObj.create_employee_type_user()
        self.employee2 = setUpObj.create_employee_type_user(username='emp2')
        self.restaurant1 = setUpObj.create_restaurant(
                        owner=self.owner,
                        name='Restaurant 1'
                    )
        self.restaurant2 = setUpObj.create_restaurant(
                        owner=self.owner,
                        name='Restaurant 2'
                    )
        self.voting_date = datetime.now().date()
        self.menu1 = setUpObj.create_menu(
            restaurant=self.restaurant1,
            upload_date=self.voting_date
        )
        self.menu2 = setUpObj.create_menu(
            restaurant=self.restaurant2,
            upload_date=self.voting_date
        )
        self.vote = setUpObj.create_vote(
            employee=self.employee1,
            menu=self.menu1,
            voting_date=self.voting_date
        )

    def update_vote_using_api(self, menu, voting_date=None):
        payload = {
            'menu': menu.pk
        }
        if voting_date:
            payload['voting_date'] = voting_date
        return self.client.patch(
            reverse(
                'api:voting-api-v1:vote-rud',
                kwargs={'pk': self.vote.pk}
            ),
            data=payload
        )

    def delete_vote_using_api(self):
        return self.client.delete(
            reverse(
                'api:voting-api-v1:vote-rud',
                kwargs={'pk': self.vote.pk}
            )
        )

    # Tests regarding GET api
    def test_only_authenticated_user_can_get_vote(self):
        response = self.client.get(
            reverse(
                'api:voting-api-v1:vote-rud',
                kwargs={'pk': self.vote.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_vote(self):
        self.client.login(
            username=self.employee1.username,
            password='password'
        )
        res = self.client.get(
            reverse(
                'api:voting-api-v1:vote-rud',
                kwargs={'pk': self.vote.pk}
            )
        )
        self.client.logout()
        vote = Vote.objects.get(pk=self.vote.pk)

        self.assertEqual(res.data['id'], vote.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_vote(self):
        self.client.login(
            username=self.employee1.username,
            password='password'
        )
        res = self.client.get(
            reverse(
                'api:voting-api-v1:vote-rud',
                kwargs={'pk': 100}
            )
        )
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # Tests regarding PUT, PATCH, DELETE api
    def test_admin_can_not_update_delete_vote(self):
        self.client.login(
            username=self.admin.username,
            password='password'
        )
        update_res = self.update_vote_using_api(self.menu2)
        delete_res = self.delete_vote_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_owner_can_not_update_delete_vote(self):
        self.client.login(username=self.owner.username, password='password')
        update_res = self.update_vote_using_api(self.menu2)
        delete_res = self.delete_vote_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_not_update_delete_vote_of_another_employee(self):
        self.client.login(
            username=self.employee2.username,
            password='password'
        )
        update_res = self.update_vote_using_api(self.menu2)
        delete_res = self.delete_vote_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_not_change_voting_date_of_his_own_vote(self):
        self.client.login(
            username=self.employee1.username,
            password='password'
        )
        update_res = self.update_vote_using_api(
                        self.menu2,
                        self.voting_date + timedelta(days=1)
                    )
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_can_update_delete_his_own_vote(self):
        self.client.login(
            username=self.employee1.username,
            password='password'
        )
        update_res = self.update_vote_using_api(self.menu2)
        delete_res = self.delete_vote_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_changing_vote_menu_adjusts_num_of_votes_of_both_the_menus(self):
        self.menu1.refresh_from_db()
        self.menu2.refresh_from_db()
        previous_num_of_votes_1 = self.menu1.num_of_votes
        previous_num_of_votes_2 = self.menu2.num_of_votes
        self.client.login(
            username=self.employee1.username,
            password='password'
        )
        res = self.update_vote_using_api(self.menu2)
        self.client.logout()
        self.menu1.refresh_from_db()
        self.menu2.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.menu1.num_of_votes, previous_num_of_votes_1 - 1)
        self.assertEqual(self.menu2.num_of_votes, previous_num_of_votes_2 + 1)
