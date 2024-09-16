from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.paginator import Paginator

from kitchen.models import DishType
from kitchen.forms import DishTypeSearchForm
from .db_test_data import dish_types


DISH_TYPES_LIST_URL = reverse("kitchen:dish-types-page")


class PrivateListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="dennie",
            first_name="Dennie",
            last_name="Denniston",
            profile_picture="dennie.jpg",
            password="testpassword"
        )

        for dish_type in dish_types:
            DishType.objects.create(
                name=dish_type["name"],
                description=dish_type["description"]
            )

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.dish_types_page_1 = self.client.get(DISH_TYPES_LIST_URL)
        self.dish_types_page_2 = self.client.get(DISH_TYPES_LIST_URL, {"page": 2})
        self.all_dish_types = DishType.objects.all()

    def test_retrieve_dish_types_per_paginated_page(self):
        self.assertEqual(self.dish_types_page_1.status_code, 200)
        self.assertEqual(len(self.dish_types_page_1.context["dish_types"]), 5)

        self.assertEqual(self.dish_types_page_2.status_code, 200)
        self.assertEqual(len(self.dish_types_page_2.context["dish_types"]), 1)

        self.assertEqual(self.all_dish_types.count(), 6)
        self.assertEqual(
            list(self.all_dish_types),
            list(self.dish_types_page_1.context["dish_types"]) +
            list(self.dish_types_page_2.context["dish_types"])
        )
        self.assertTemplateUsed(self.dish_types_page_1, "kitchen/dish_type_list.html")

    def test_dish_type_list_contains_correct_data_per_paginated_page(self):
        first_page_5_dish_types = self.all_dish_types[:5]
        last_page_1_dish_type = self.all_dish_types[5]
        
        self.assertEqual(self.dish_types_page_1.status_code, 200)
        for dish_type in first_page_5_dish_types:
            self.assertContains(self.dish_types_page_1, dish_type.name)
        self.assertNotContains(self.dish_types_page_1, last_page_1_dish_type.name)

        self.assertEqual(self.dish_types_page_2.status_code, 200)
        self.assertContains(self.dish_types_page_2, last_page_1_dish_type.name)
        for dish_type in first_page_5_dish_types:
            self.assertNotContains(self.dish_types_page_2, dish_type.name)

        self.assertIsInstance(
            self.dish_types_page_1.context["paginator"],
            Paginator
        )
        self.assertEqual(
            str(self.dish_types_page_1.context["page_obj"]),
            "<Page 1 of 2>"
        )
        self.assertTrue(self.dish_types_page_1.context["is_paginated"])

    def test_dish_type_get_context_data_receives_correct_search_form(self):
        response = self.client.get(DISH_TYPES_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], DishTypeSearchForm)

    def test_dish_type_get_queryset_with_valid_search_form(self):
        response = self.client.get(DISH_TYPES_LIST_URL, {"name": "cake"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cake")
        for dish_type in self.all_dish_types:
            if dish_type.name != "cake":
                self.assertNotContains(response, dish_type.name)

    def test_dish_type_get_queryset_with_invalid_search_form(self):
        response = self.client.get(DISH_TYPES_LIST_URL, {"name": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "invalid")
        for dish_type in self.all_dish_types:
            self.assertNotContains(response, dish_type.name)
