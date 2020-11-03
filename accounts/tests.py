from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.


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