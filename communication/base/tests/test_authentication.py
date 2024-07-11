from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class UserAuthenticationTests(TestCase):

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'testpassword',
            'email': 'test@email.com',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)
