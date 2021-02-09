from unittest import TestCase

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.urls import reverse, resolve

# Create your tests here.
from pages.forms import UserProfilForm
from pages.models import UserProfile
from pages.views import LandingView, ProfilPage


class HomepageTests(SimpleTestCase):
    databases = '__all__'

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_url_resolves(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, LandingView.as_view().__name__)

class ProfilePageTests(SimpleTestCase):
    databases = '__all__'

    def setUp(self):
        self.client.login(email='test_user2@email.com', password='1234')
        url = reverse('profilPage')
        self.response = self.client.get(url)

    def test_profilpage_status_code(self):
        self.assertEqual(self.response.status_code, 302)
        self.assertRedirects(self.response, '/profil/#form')

    def test_profilpage_url_resolves(self):
        view = resolve('/profilView/')
        self.assertEqual(view.func.__name__, ProfilPage.as_view().__name__)