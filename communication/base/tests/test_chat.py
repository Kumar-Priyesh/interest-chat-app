# test_chat.py
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Message, Interest

class ChatFunctionalityTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.interest = Interest.objects.create(sender=self.user1, receiver=self.user2, accepted=True)
        self.client.login(username='user1', password='password1')

    def test_send_message(self):
        response = self.client.post(reverse('send_message', args=[self.interest.id]), {
            'message': 'Hello!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(sender=self.user1, receiver=self.user2, content='Hello!').exists())
    
    def test_recieve_message(self):
        url = reverse('chat', args=[self.interest.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
