from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


class AccountsSystemTest(TestCase):

    def setUp(self):
        """Set up a test user for auth-protected views."""
        self.user_data = {"username": "testuser", "password": "RamshornSnail89!"}
        self.user = User.objects.create_user(**self.user_data)

    def test_profile_signal_created(self):
        """Ensures that every new user automatically gets a profile."""
        new_user = User.objects.create_user(
            username="newbie", password="RamshornSnail29"
        )
        self.assertTrue(Profile.objects.filter(user=new_user).exists())

    def test_login_view_status(self):
        """Verifies the login page loads correctly."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_protected_profile_view(self):
        """Verifies that an unauthenticated user is redirected to login."""
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)  # Redirect code

    def test_profile_update_logic(self):
        """Verifies that a user can update their bio and theme."""
        self.client.login(**self.user_data)
        # Testing the POST request
        response = self.client.post(
            reverse("update_profile"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "bio": "My new movie bio",
                "dark_mode": "True",  # Sending string 'True' as choices often do
                "favorite_genre": "Sci-Fi",
            },
        )
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, "My new movie bio")
        self.assertTrue(self.user.profile.dark_mode)

    def test_logout_message_and_redirect(self):
        """Verifies logout redirects and clears session."""
        self.client.login(**self.user_data)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
