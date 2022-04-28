import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import CustomUser


class CustomUserRegisterTestApi(TestCase):
    """ Test module for checking permission of user creation. """

    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            username='test_admin',
            password='password',
            user_type=CustomUser.UserType.ADMIN
        )
        self.employee_user = CustomUser.objects.create_user(
            username='test_employee',
            password='password',
            user_type=CustomUser.UserType.EMPLOYEE
        )
        self.restaurant_owner_user = CustomUser.objects.create_user(
            username='test_owner',
            password='password',
            user_type=CustomUser.UserType.RESTAURANT_OWNER
        )
        self.payload = {
            'username': 'admin1',
            'password1': 'password',
            'password2': 'password',
            'user_type': CustomUser.UserType.ADMIN
        }

    def create_admin(self):
        return self.client.post(
            reverse('api:user-api-v1:rest_register'),
            data=json.dumps(self.payload),
            content_type='application/json'
        )

    def create_employee(self):
        self.payload['username'] = 'emp1'
        self.payload['user_type'] = CustomUser.UserType.EMPLOYEE
        return self.client.post(
            reverse('api:user-api-v1:rest_register'),
            data=json.dumps(self.payload),
            content_type='application/json'
        )

    def create_restaurant_owner(self):
        self.payload['username'] = 'res_own1'
        self.payload['user_type'] = CustomUser.UserType.RESTAURANT_OWNER
        return self.client.post(
            reverse('api:user-api-v1:rest_register'),
            data=json.dumps(self.payload),
            content_type='application/json'
        )

    def test_only_authenticated_user_can_post_register(self):
        res = self.create_admin()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_any_type_user(self):
        self.client.login(
            username=self.admin_user.username,
            password='password'
        )
        res1 = self.create_admin()
        res2 = self.create_employee()
        res3 = self.create_restaurant_owner()
        self.client.logout()

        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res3.status_code, status.HTTP_201_CREATED)

    def test_employee_cannot_create_any_user(self):
        self.client.login(
            username=self.employee_user.username,
            password='password'
        )
        res1 = self.create_admin()
        res2 = self.create_employee()
        res3 = self.create_restaurant_owner()
        self.client.logout()

        self.assertEqual(res1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res3.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_owner_cannot_create_any_user(self):
        self.client.login(
            username=self.restaurant_owner_user.username,
            password='password'
        )
        res1 = self.create_admin()
        res2 = self.create_employee()
        res3 = self.create_restaurant_owner()
        self.client.logout()

        self.assertEqual(res1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res3.status_code, status.HTTP_403_FORBIDDEN)
