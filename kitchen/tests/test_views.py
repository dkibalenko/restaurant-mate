from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from urllib.parse import urlparse, parse_qs


class PublicAccessViewTest(TestCase):
    def test_main_page_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("kitchen:main-page"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=%2F")

    def test_cook_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("kitchen:cooks-page"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fcooks%2F"
        )

    def test_dish_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("kitchen:dishes-page"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fdishes%2F"
        )

    def test_dish_type_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("kitchen:dish-types-page"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fdish_types%2F"
        )
    
    def test_ingredient_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("kitchen:ingredients-page"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fingredients%2F"
        )


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
        response = self.client.get(reverse("kitchen:main-page"))
        expected_redirect_url = (
            f"{reverse('login')}?"
            f"next=/{reverse('kitchen:main-page')}/"
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
