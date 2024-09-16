from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.paginator import Paginator

from kitchen.models import Ingredient
from kitchen.forms import IngredientSearchForm
from .db_test_data import ingredients


INGREDIENTS_LIST_URL = reverse("kitchen:ingredients-page")


class PrivateIngredientListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username="dennie",
            first_name="Dennie",
            last_name="Denniston",
            profile_picture="dennie.jpg",
            password="testpassword"
        )

        for ingredient in ingredients:
            Ingredient.objects.create(
                name=ingredient["name"],
                description=ingredient["description"]
            )

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.ingredients_page_1 = self.client.get(INGREDIENTS_LIST_URL)
        self.ingredients_page_2 = self.client.get(
            INGREDIENTS_LIST_URL, {"page": 2})
        self.all_ingredients = Ingredient.objects.all()

    def test_retrieve_ingredients_per_paginated_page(self):
        self.assertEqual(self.ingredients_page_1.status_code, 200)
        self.assertEqual(
            len(self.ingredients_page_1.context["ingredients"]), 5)

        self.assertEqual(self.ingredients_page_2.status_code, 200)
        self.assertEqual(
            len(self.ingredients_page_2.context["ingredients"]), 1)

        self.assertEqual(self.all_ingredients.count(), 6)
        self.assertEqual(
            list(self.all_ingredients),
            list(self.ingredients_page_1.context["ingredients"])
            + list(self.ingredients_page_2.context["ingredients"])
        )
        self.assertTemplateUsed(self.ingredients_page_1,
                                "kitchen/ingredient_list.html")

    def test_ingredient_list_contains_correct_data_per_paginated_page(self):
        first_page_5_ingredients = self.all_ingredients[:5]
        last_page_1_ingredient = self.all_ingredients[5]

        self.assertEqual(self.ingredients_page_1.status_code, 200)
        for ingredient in first_page_5_ingredients:
            self.assertContains(self.ingredients_page_1, ingredient.name)
        self.assertNotContains(self.ingredients_page_1,
                               last_page_1_ingredient.name)

        self.assertEqual(self.ingredients_page_2.status_code, 200)
        self.assertContains(self.ingredients_page_2,
                            last_page_1_ingredient.name)
        for ingredient in first_page_5_ingredients:
            self.assertNotContains(self.ingredients_page_2, ingredient.name)

        self.assertIsInstance(
            self.ingredients_page_1.context["paginator"],
            Paginator
        )
        self.assertEqual(
            str(self.ingredients_page_1.context["page_obj"]),
            "<Page 1 of 2>"
        )
        self.assertTrue(self.ingredients_page_1.context["is_paginated"])

    def test_ingredient_get_context_data_receives_correct_search_form(self):
        response = self.client.get(INGREDIENTS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"], IngredientSearchForm)

    def test_ingredient_get_queryset_with_valid_search_form(self):
        response = self.client.get(INGREDIENTS_LIST_URL, {"name": "water"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "water")
        for ingredient in self.all_ingredients:
            if ingredient.name != "water":
                self.assertNotContains(response, ingredient.name)

    def test_ingredient_get_queryset_with_invalid_search_form(self):
        response = self.client.get(INGREDIENTS_LIST_URL, {"name": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "invalid")
        for ingredient in self.all_ingredients:
            self.assertNotContains(response, ingredient.name)

    def test_ingredient_get_queryset_with_no_search_form_data(self):
        self.assertEqual(
            list(self.all_ingredients),
            list(self.ingredients_page_1.context["ingredients"])
            + list(self.ingredients_page_2.context["ingredients"])
        )
