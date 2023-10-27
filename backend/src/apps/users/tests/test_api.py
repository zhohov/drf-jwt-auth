from typing import NoReturn

from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User
from apps.users.serializers import UserSerializer


class UserAPITests(APITestCase):
    def setUp(self) -> NoReturn:
        self.url = '/api/users/'
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='test_password'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='test_password'
        )
        self.data = {
            'username': 'user3',
            'email': 'user3@example.com',
            'password': 'test_password',
        }

    def test_set_user(self) -> NoReturn:
        response = self.client.post(path=self.url, data=self.data, format='json')
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(response.data, {'username': 'user3', 'email': 'user3@example.com'})

    def test_get_users(self) -> NoReturn:
        self.test_set_user()
        response = self.client.get(path=self.url)
        serializer_data = UserSerializer([self.user1, self.user2, self.data], many=True).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

    def test_get_user_by_pk(self) -> NoReturn:
        response = self.client.get(path=self.url+'1/')
        serializer_data = UserSerializer(self.user1).data
        self.assertEquals(serializer_data, response.data)

    def test_get_user_by_pk_not_found(self):
        response = self.client.get(path=self.url + '5/')
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
