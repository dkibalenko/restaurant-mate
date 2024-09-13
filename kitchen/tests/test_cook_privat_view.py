from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.forms import CookSearchForm

COOKS_LIST_URL = reverse("kitchen:cooks-page")


class PrivateCookViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="dennie",
            first_name="Dennie",
            last_name="Denniston",
            profile_picture="dennie.png",
            password="testpassword"
        )
        self.client.force_login(self.user)

    # def test_cook_get_context_data_receives_correct_search_form(self):
    #     response = self.client.get(COOKS_LIST_URL)
    #     self.assertIsInstance(response.context["search_form"], CookSearchForm)

    # def test_cook_get_queryset_with_valid_search_form(self):
    #     response = self.client.get(COOKS_LIST_URL, {"username": "dennie"})
