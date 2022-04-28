import tempfile
from django.core.files import File
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from user.models import CustomUser
from voting.models import Menu, Restaurant, Vote, Result


class SetUpModel:
    """
    Base class for common db model creation.
    """

    def create_admin_type_user(self, username='test_admin'):
        return CustomUser.objects.create_user(
            username=username,
            password='password',
            user_type=CustomUser.UserType.ADMIN
        )

    def create_employee_type_user(self, username='test_employee'):
        return CustomUser.objects.create_user(
            username=username,
            password='password',
            user_type=CustomUser.UserType.EMPLOYEE
        )

    def create_restaurant_owner_type_user(self, username='test_owner'):
        return CustomUser.objects.create_user(
            username=username,
            password='password',
            user_type=CustomUser.UserType.RESTAURANT_OWNER
        )

    def create_restaurant(self, owner, name='Test Restaurant'):
        return Restaurant.objects.create(
            owner=owner,
            name=name
        )

    def create_menu(self, restaurant, upload_date):
        menu_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        return Menu.objects.create(
            restaurant=restaurant,
            menu_image=menu_image,
            upload_date=upload_date
        )

    def create_vote(self, employee, menu, voting_date):
        return Vote.objects.create(
            employee=employee,
            menu=menu,
            voting_date=voting_date
        )

    def create_result(self, voting_date):
        return Result.objects.create(
            voting_date=voting_date
        )

    def create_file(self, filename='test.jpeg', filepath=None):
        if filepath is None:
            filepath = settings.BASE_DIR / 'test_file/test.jpeg'
        file = File(open(filepath, 'rb'))
        uploaded_file = SimpleUploadedFile(
                        filename,
                        file.read(),
                        content_type='multipart/form-data'
                    )
        return uploaded_file
