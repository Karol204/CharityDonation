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
        url = reverse('profil')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'profil.html')
