from rest_framework import status
from rest_framework.test import APITransactionTestCase
from django.urls import reverse
from voting.models import Restaurant
from voting.api.v1.serializers import RestaurantSerializer
from voting.tests.base_setup_model import SetUpModel


class RestaurantListCreateAPITest(APITransactionTestCase):
    """ Test module for list create API of the restaurant model. """

    def setUp(self):
        setUpObj = SetUpModel()
        self.admin = setUpObj.create_admin_type_user()
        self.owner = setUpObj.create_restaurant_owner_type_user()
        self.employee = setUpObj.create_employee_type_user()
        setUpObj.create_restaurant(owner=self.owner, name='Restaurant 1')
        setUpObj.create_restaurant(owner=self.owner, name='Restaurant 2')
        setUpObj.create_restaurant(owner=self.owner, name='Restaurant 3')

    def create_restaurant_using_api(self):
        payload = {
            'name': 'Restaurant1'
        }
        return self.client.post(
            reverse('api:voting-api-v1:restaurant-list-create'),
            data=payload,
            format='json'
        )

    # Tests regarding GET api
    def test_only_authenticated_user_can_get_restaurants(self):
        response = self.client.get(
            reverse('api:voting-api-v1:restaurant-list-create')
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_restaurants(self):
        self.client.login(username=self.employee.username, password='password')
        res = self.client.get(
            reverse('api:voting-api-v1:restaurant-list-create')
        )
        self.client.logout()
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Tests regarding POST api
    def test_admin_can_not_create_restaurants(self):
        self.client.login(username=self.admin.username, password='password')
        res = self.create_restaurant_using_api()
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_not_create_restaurants(self):
        self.client.login(username=self.employee.username, password='password')
        res = self.create_restaurant_using_api()
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_owner_can_create_restaurants(self):
        self.client.login(username=self.owner.username, password='password')
        res = self.create_restaurant_using_api()
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class RestaurantRUDAPITest(APITransactionTestCase):
    """ Test module for RUD API of the restaurant model. """

    def setUp(self):
        setUpObj = SetUpModel()
        self.admin = setUpObj.create_admin_type_user()
        self.owner = setUpObj.create_restaurant_owner_type_user()
        self.no_owner = setUpObj.create_restaurant_owner_type_user(
                        username='test_owner_2'
                    )
        self.employee = setUpObj.create_employee_type_user()
        self.restaurant = setUpObj.create_restaurant(
                            owner=self.owner,
                            name='Restaurant 1'
                        )

    def update_restaurant_using_api(self, name='New Name'):
        payload = {
            'name': name
        }
        return self.client.put(
            reverse(
                'api:voting-api-v1:restaurant-rud',
                kwargs={'pk': self.restaurant.pk}
            ),
            data=payload,
            format='json'
        )

    def delete_restaurant_using_api(self):
        return self.client.delete(
            reverse(
                'api:voting-api-v1:restaurant-rud',
                kwargs={'pk': self.restaurant.pk}
            )
        )

    # Tests regarding GET api
    def test_only_authenticated_user_can_get_restaurant(self):
        response = self.client.get(
            reverse(
                'api:voting-api-v1:restaurant-rud',
                kwargs={'pk': self.restaurant.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_restaurant(self):
        self.client.login(username=self.employee.username, password='password')
        res = self.client.get(
            reverse(
                'api:voting-api-v1:restaurant-rud',
                kwargs={'pk': self.restaurant.pk}
            )
        )
        self.client.logout()
        restaurant = Restaurant.objects.get(pk=self.restaurant.pk)
        serializer = RestaurantSerializer(restaurant)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_restaurant(self):
        self.client.login(username=self.employee.username, password='password')
        res = self.client.get(
            reverse(
                'api:voting-api-v1:restaurant-rud',
                kwargs={'pk': 100}
            )
        )
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # Tests regarding PUT, PATCH, DELETE api
    def test_admin_can_not_update_delete_restaurant(self):
        self.client.login(username=self.admin.username, password='password')
        update_res = self.update_restaurant_using_api()
        delete_res = self.delete_restaurant_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_not_update_delete_restaurant(self):
        self.client.login(username=self.employee.username, password='password')
        update_res = self.update_restaurant_using_api()
        delete_res = self.delete_restaurant_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_owner_of_the_restaurant_can_not_update_delete_restaurant(self):
        self.client.login(username=self.no_owner.username, password='password')
        update_res = self.update_restaurant_using_api()
        delete_res = self.delete_restaurant_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_of_the_restaurant_can_update_delete_restaurant(self):
        self.client.login(username=self.owner.username, password='password')
        update_res = self.update_restaurant_using_api(name='New Name')
        delete_res = self.delete_restaurant_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertEqual(update_res.data['name'], 'New Name')
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
