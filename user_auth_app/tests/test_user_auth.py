from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from users_app.models import CustomUser
from user_auth_app.tasks import send_password_reset_email, send_confirmation_email


class UserAuthTests(APITestCase):
    
    def setUp(self):
        self.get_queue_patcher = patch('django_rq.get_queue')
        self.mocked_get_queue = self.get_queue_patcher.start()
        self.user = CustomUser.objects.create_user(username='test@user.de', email='test@user.de', password='test123')


    def tearDown(self):
        self.get_queue_patcher.stop()


    def test_register_user(self):
        self.mocked_get_queue.return_value.enqueue.reset_mock()
        queue = self.mocked_get_queue.return_value
        url = reverse('registration')
        data = {
            'email': 'test2@user.de',
            'password': 'test1234',
            'repeated_password': 'test1234'
        }
        response = self.client.post(url, data, format='json')
        queue.enqueue.assert_called_once_with(send_confirmation_email, response.data['email'], response.data['email'], response.data['token'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(response.data['user_id'], CustomUser.objects.get(email=data['email']).id)


    def test_login_unconfirmed_user(self):
        url = reverse('login')
        data = {
            'username': 'test@user.de',
            'password': 'test123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_login_confirmed_user(self):
        self.user.confirmed = True
        self.user.save(update_fields=['confirmed'])
        url = reverse('login')
        data = {
            'username': 'test@user.de',
            'password': 'test123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], self.user.id)


    def test_login_wrong_credentials(self):
        url = reverse('login')
        data = {
            'username': 'test@user.de',
            'password': 'test456'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_activate_user(self):
        url = reverse('activate', kwargs={'token': self.user.auth_token.key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


    def test_forgot_password(self):
        self.mocked_get_queue.return_value.enqueue.reset_mock()
        queue = self.mocked_get_queue.return_value
        url = reverse('forgot-password')
        data = {
            'email': 'test@user.de'
        }
        response = self.client.post(url, data, format='json')
        queue.enqueue.assert_called_once_with(send_password_reset_email, data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_forgot_password_wrong_credentials(self):
        url = reverse('forgot-password')
        data = {
            'email': 'test123@user.de'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_reset_password(self):
        url = reverse('reset-password')
        data = {
            'email': 'test@user.de',
            'new_password': 'neu123',
            'repeated_password': 'neu123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_reset_password_no_user(self):
        url = reverse('reset-password')
        data = {
            'email': 'test123@user.de',
            'new_password': 'neu123',
            'repeated_password': 'neu123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_reset_password_wrong_password(self):
        url = reverse('reset-password')
        data = {
            'email': 'test@user.de',
            'new_password': 'neu123',
            'repeated_password': 'neu1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
