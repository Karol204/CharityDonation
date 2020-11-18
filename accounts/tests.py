from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.
from django.urls import reverse, reverse_lazy

from accounts.forms import CustomUserCreationForm


class CustomUserTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='Karol',
            email='karol@email.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'Karol')
        self.assertEqual(user.email, 'karol@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='Superadmin',
            email='superadmin@email.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'Superadmin')
        self.assertEqual(user.email, 'superadmin@email.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

class SignUpTest(TestCase):

    username = 'newtestuser'
    email = 'newtestuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)

        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csfrmiddlewaretoken')