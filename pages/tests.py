from unittest import TestCase

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.
from pages.forms import UserProfilForm
from pages.models import UserProfile


class HomepageTests(SimpleTestCase):
    databases = '__all__'

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'home.html')

class ProfilePageTests(SimpleTestCase):
    databases = '__all__'

    def setUp(self):
        guest = get_user_model().objects.create_user(username='test_user1', email='test_user1@email.com', password='1234')
        url = reverse('profilpage')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 302)
        self.assertRedirects(self.response, '/profil/#form')
#
# class AccountDetailViewTests(SimpleTestCase):
#
#     databases = '__all__'
#     def setUp(self):
#         guest = get_user_model().objects.create_user(username='test_user12', email='test_user12@email.com', password='1234')
#         guest_other = get_user_model().objects.create_user(username='test_user3', email='test_user3@email.com', password='5678')
#
#     def test_login_required_redirection(self):
#
#         self.url = reverse('profilpage')
#         login_url = reverse('account_login')
#         response = self.client.get(self.url)
#
#     def test_logged_in_uses_correct_template(self):
#
#         login = self.client.login(username='john.doe', password='1234')
#         response = self.client.get(reverse('profilpage'))
#         self.assertEqual(str(response.context['user']), 'john.doe')
#         self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profil.html')
