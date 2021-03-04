from datetime import datetime
from functools import wraps
from urllib.parse import urlencode

from django.urls import reverse
from django.contrib.auth.models import User as AuthUser
from rest_framework.test import APITestCase
from rest_framework import status
from parameterized import parameterized, param
from rest_framework.authtoken.models import Token

from .models import Doctor, Drug, Pharmacy, Booking, User


def valid_token_auth(f):
    @wraps(f)
    def _wrap(self, *args, **kwargs):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.valid_token}')
        return f(self, *args, **kwargs)
    return _wrap


class PrescriptionApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        doctor = Doctor.objects.create(
            first_name='Doctor', last_name='Test', email='doc@email.com',
            reg_number='F19832791', date_of_birth=datetime(1969, 11, 23)
        )

        drug = Drug.objects.create(name='Test Drug Name')

        pharmacy = Pharmacy.objects.create(name='Test Pharmacy Name')

        cls.users = {}
        for first_name, dob, address in (
            ('Bob', datetime(1965, 11, 23), 'a1'),
            ('John', datetime(1975, 11, 23), 'b2'),
            ('Jane', datetime(1985, 11, 23), 'c3'),
        ):
            user = cls.users[first_name] = User.objects.create(
                first_name=first_name, last_name='Test', date_of_birth=dob,
                email=f'{first_name.lower()}@email.com', address=address
            )
            # create one booking per user:
            Booking.objects.create(
                user=user, doctor=doctor, pharmacy=pharmacy, drug=drug)

        authuser, _ = AuthUser.objects.get_or_create(username='admin')
        token, _ = Token.objects.get_or_create(user=authuser)
        cls.valid_token = token.key

    def get(self, url, expected_status):
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_status, response.data)
        return response

    @parameterized.expand([
        param('Invalid token', is_token_valid=False,
              expected_status=status.HTTP_401_UNAUTHORIZED),
        param('Valid token', is_token_valid=True,
              expected_status=status.HTTP_200_OK),
        param('No token provided', is_token_valid=None,
              expected_status=status.HTTP_401_UNAUTHORIZED),
    ])
    def test_01_user_auth(self, _, is_token_valid, expected_status):
        url = reverse('user-list')
        if is_token_valid is None:
            self.client.credentials()
        elif not is_token_valid:
            self.client.credentials(HTTP_AUTHORIZATION='Token 123')
        else:
            self.client.credentials(
                HTTP_AUTHORIZATION=f'Token {self.valid_token}')
        self.get(url, expected_status)

    @parameterized.expand([
        param('retrieve all', search=None, expected_count=3),
        param('search for J', search='J', expected_count=2),  # John and Jane
        param('search for Z', search='Z', expected_count=0),
    ])
    @valid_token_auth
    def test_02_user_list(self, _, search, expected_count):
        url = reverse('user-list')
        if search:
            url += f'?search={search}'
        response = self.get(url, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected_count)

    @parameterized.expand([
        param('retrieve all', user_name=None, expected_count=3),
        param('search for Bob', user_name="Bob", expected_count=1),
    ])
    @valid_token_auth
    def test_03_booking_list(self, _, user_name, expected_count):
        url = reverse('booking-list')
        if user_name:
            filter = {'user_id': User.objects.get(first_name=user_name).id}
            url += '?' + urlencode(filter)
        response = self.get(url, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected_count)
