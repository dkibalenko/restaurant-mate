from urllib.parse import urlparse, parse_qs
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

MAIN_PAGE_URL = reverse("kitchen:main-page")


class CustomLogoutViewTest(TestCase):
    def setUp(self):
        self.cook = get_user_model().objects.create_user(
            username="dennie",
            password="testpassword"
        )
        self.client.login(username="dennie", password="testpassword")

    def test_get_logout_view(self):
        response  = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/logged_out.html")

    def test_post_logout_view(self):
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_user_is_logged_out(self):
        self.client.post(reverse("logout"))
        response = self.client.get(MAIN_PAGE_URL)
        expected_redirect_url = (
            f"{reverse('login')}?"
            f"next=/{MAIN_PAGE_URL}/"
        )

        parsed_response_url = urlparse(response.url)
        parsed_expected_redirect_url = urlparse(expected_redirect_url)

        self.assertEqual(
            parsed_response_url.path, 
            parsed_expected_redirect_url.path
        )

        response_next_parameter = (
            parse_qs(parsed_response_url.query).get("next", [""])[0]
            .rstrip("/")
        )
        expected_redirect_url_next_parameter = (
            parse_qs(parsed_expected_redirect_url.query).get("next", [""])[0]
            .rstrip("/")
        )

        self.assertEqual(
            response_next_parameter, 
            expected_redirect_url_next_parameter
        )
