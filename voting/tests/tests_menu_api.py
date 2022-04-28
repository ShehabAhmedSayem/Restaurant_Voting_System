from datetime import datetime, timedelta
from rest_framework.test import APITransactionTestCase
from rest_framework import status
from django.urls import reverse
from voting.models import Menu
from voting.tests.base_setup_model import SetUpModel


class MenuListCreateAPITest(APITransactionTestCase):
    """ Test module for list create API of the Menu model. """

    def setUp(self):
        setUpObj = SetUpModel()
        self.file = setUpObj.create_file()
        self.admin = setUpObj.create_admin_type_user()
        self.owner = setUpObj.create_restaurant_owner_type_user()
        self.no_owner = setUpObj.create_restaurant_owner_type_user(
                        username='test_owner_2'
                    )
        self.employee = setUpObj.create_employee_type_user()
        self.restaurant1 = setUpObj.create_restaurant(
                        owner=self.owner,
                        name='Restaurant 1'
                    )
        self.restaurant2 = setUpObj.create_restaurant(
                        owner=self.owner,
                        name='Restaurant 2'
                    )
        self.upload_date = datetime.now().date()
        self.menu1 = setUpObj.create_menu(
            restaurant=self.restaurant1,
            upload_date=self.upload_date
        )
        self.menu2 = setUpObj.create_menu(
            restaurant=self.restaurant2,
            upload_date=self.upload_date
        )

    def create_menu_using_api(self, restaurant, date=datetime.now().date()):
        payload = {
            'restaurant': restaurant.pk,
            'menu_image': self.file,
            'upload_date': date
        }
        return self.client.post(
            reverse('api:voting-api-v1:menu-list-create'),
            data=payload
        )

    # Tests regarding GET api
    def test_only_authenticated_user_can_get_menus(self):
        response = self.client.get(
            reverse('api:voting-api-v1:menu-list-create')
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_menus(self):
        self.client.login(username=self.employee.username, password='password')
        res = self.client.get(
            reverse('api:voting-api-v1:menu-list-create')
        )
        self.client.logout()
        total_menu = Menu.objects.all().count()
        self.assertEqual(len(res.data), total_menu)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Tests regarding POST api
    def test_admin_can_not_create_menus(self):
        self.client.login(username=self.admin.username, password='password')
        res = self.create_menu_using_api(restaurant=self.restaurant1)
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_not_create_menus(self):
        self.client.login(username=self.employee.username, password='password')
        res = self.create_menu_using_api(restaurant=self.restaurant1)
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_restaurant_owner_can_not_create_menus_of_the_restaurant(self):
        self.client.login(username=self.no_owner.username, password='password')
        res = self.create_menu_using_api(restaurant=self.restaurant1)
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_owner_can_create_menus_of_the_restaurant(self):
        self.client.login(username=self.owner.username, password='password')
        res = self.create_menu_using_api(
                restaurant=self.restaurant1,
                date=self.upload_date + timedelta(days=1)
            )
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_restaurant_owner_can_create_only_one_menu_per_day(self):
        self.client.login(username=self.owner.username, password='password')
        res = self.create_menu_using_api(
                restaurant=self.restaurant1,
                date=self.upload_date
            )
        self.client.logout()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class MenuRUDAPITest(APITransactionTestCase):
    """ Test module for RUD API of the menu model. """

    def setUp(self):
        setUpObj = SetUpModel()
        self.file = setUpObj.create_file()
        self.admin = setUpObj.create_admin_type_user()
        self.owner1 = setUpObj.create_restaurant_owner_type_user()
        self.owner2 = setUpObj.create_restaurant_owner_type_user(
                        username='test_owner_2'
                    )
        self.employee = setUpObj.create_employee_type_user()
        self.restaurant1 = setUpObj.create_restaurant(
                        owner=self.owner1,
                        name='Restaurant 1'
                    )
        self.restaurant2 = setUpObj.create_restaurant(
                        owner=self.owner2,
                        name='Restaurant 2'
                    )
        self.upload_date = datetime.now().date()
        self.menu = setUpObj.create_menu(
            restaurant=self.restaurant1,
            upload_date=self.upload_date
        )

    def update_menu_using_api(self, image, upload_date=None):
        payload = {
            'menu_image': image,
        }
        if upload_date:
            payload['upload_date'] = upload_date
        return self.client.patch(
            reverse(
                'api:voting-api-v1:menu-rud',
                kwargs={'pk': self.menu.pk}
            ),
            data=payload
        )

    def delete_menu_using_api(self):
        return self.client.delete(
            reverse(
                'api:voting-api-v1:menu-rud',
                kwargs={'pk': self.menu.pk}
            )
        )

    # Tests regarding GET api
    def test_only_authenticated_user_can_get_menu(self):
        response = self.client.get(
            reverse(
                'api:voting-api-v1:menu-rud',
                kwargs={'pk': self.menu.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_menu(self):
        self.client.login(username=self.employee.username, password='password')
        res = self.client.get(
            reverse(
                'api:voting-api-v1:menu-rud',
                kwargs={'pk': self.menu.pk}
            )
        )
        self.client.logout()
        menu = Menu.objects.get(pk=self.menu.pk)

        self.assertEqual(res.data['id'], menu.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_menu(self):
        self.client.login(username=self.employee.username, password='password')
        res = self.client.get(
            reverse(
                'api:voting-api-v1:menu-rud',
                kwargs={'pk': 100}
            )
        )
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # Tests regarding PUT, PATCH, DELETE api
    def test_admin_can_not_update_delete_menu(self):
        self.client.login(username=self.admin.username, password='password')
        update_res = self.update_menu_using_api(self.file)
        delete_res = self.delete_menu_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_not_update_delete_menu(self):
        self.client.login(username=self.employee.username, password='password')
        update_res = self.update_menu_using_api(self.file)
        delete_res = self.delete_menu_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_owner_of_the_restaurant_can_not_update_delete_menu(self):
        self.client.login(username=self.owner2.username, password='password')
        update_res = self.update_menu_using_api(self.file)
        delete_res = self.delete_menu_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_of_the_restaurant_can_not_change_upload_date(self):
        self.client.login(username=self.owner1.username, password='password')
        update_res = self.update_menu_using_api(
                        self.file,
                        self.upload_date + timedelta(days=1)
                    )
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_of_the_restaurant_can_update_delete_menu(self):
        self.client.login(username=self.owner1.username, password='password')
        update_res = self.update_menu_using_api(self.file)
        delete_res = self.delete_menu_using_api()
        self.client.logout()

        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
