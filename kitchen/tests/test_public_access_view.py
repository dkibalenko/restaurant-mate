from django.test import TestCase
from django.urls import reverse


class PublicViewTest(TestCase):
    def test_index_login_required_and_redirect_to_login_page(self):
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
