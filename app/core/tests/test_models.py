from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Creates a new test class"""

    def test_create_user_email_succesful(self):
        """Test creating a new user with an email is succesful"""
        email = "test@test.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email of the new user is normalized"""
        email = "test@TEST.COM"
        user = get_user_model().objects.create_user(email, "Test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "Test123")

    def test_superuser_has_is_staff_and_superuser_settings(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser("test@test.com", "Test123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
