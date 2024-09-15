from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.paginator import Paginator

from kitchen.models import Dish, DishType, Ingredient
from kitchen.forms import CookSearchForm
from .db_test_data import users, dish_data

COOKS_LIST_URL = reverse("kitchen:cooks-page")


class PrivateCookViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="dennie",
            first_name="Dennie",
            last_name="Denniston",
            profile_picture="dennie.jpg",
            password="testpassword"
        )

        for user in users:
            get_user_model().objects.create_user(
                username=user["username"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                profile_picture=user["profile_picture"],
                password=user["password"]
            )

        cls.dish_type = DishType.objects.create(
            name="Main Course", 
            description="Main course dishes"
        )
        
        cls.ingredient1 = Ingredient.objects.create(
            name="Tomato", 
            description="Fresh tomato"
        )
        cls.ingredient2 = Ingredient.objects.create(
            name="Cheese", 
            description="Cheddar cheese"
        )

        for data in dish_data:
            dish = Dish.objects.create(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                dish_type=cls.dish_type,
                image=data["image"]
            )
            dish.ingredients.add(cls.ingredient1, cls.ingredient2)

        cls.pizza = Dish.objects.get(name="Pizza")

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.cooks_page_1 = self.client.get(COOKS_LIST_URL)
        self.cooks_page_2 = self.client.get(COOKS_LIST_URL, {"page": 2})
        self.all_cooks = get_user_model().objects.all()

    def test_retrieve_cooks_per_paginated_page(self):
        self.assertEqual(self.cooks_page_1.status_code, 200)
        self.assertEqual(len(self.cooks_page_1.context["cooks"]), 6)

        self.assertEqual(self.cooks_page_2.status_code, 200)
        self.assertEqual(len(self.cooks_page_2.context["cooks"]), 1)

        self.assertEqual(self.all_cooks.count(), 7)
        self.assertEqual(
            list(self.all_cooks),
            list(self.cooks_page_1.context["cooks"]) +
            list(self.cooks_page_2.context["cooks"])
        )
        self.assertTemplateUsed(self.cooks_page_1, "kitchen/all_cooks.html")

    def test_cook_list_contains_correct_cooks_per_paginated_page(self):
        first_page_6_cooks = self.all_cooks[:6]
        last_page_1_cook = self.all_cooks[6]
        
        self.assertEqual(self.cooks_page_1.status_code, 200)
        for cook in first_page_6_cooks:
            self.assertContains(self.cooks_page_1, cook.username)
        self.assertNotContains(self.cooks_page_1, last_page_1_cook.username)

        self.assertEqual(self.cooks_page_2.status_code, 200)
        self.assertContains(self.cooks_page_2, last_page_1_cook.username)
        for cook in first_page_6_cooks:
            if cook.username != "dennie":
                self.assertNotContains(self.cooks_page_2, cook.username)

        self.assertIsInstance(
            self.cooks_page_1.context["paginator"],
            Paginator
        )
        self.assertEqual(
            str(self.cooks_page_1.context["page_obj"]),
            "<Page 1 of 2>"
        )
        self.assertTrue(self.cooks_page_1.context["is_paginated"])

    def test_cook_get_context_data_receives_correct_search_form(self):
        response = self.client.get(COOKS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], CookSearchForm)

    def test_cook_get_queryset_with_valid_search_form(self):
        response = self.client.get(COOKS_LIST_URL, {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertNotContains(response, "ray")

    def test_cook_get_queryset_with_invalid_search_form(self):
        response = self.client.get(COOKS_LIST_URL, {"username": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "john")
        self.assertNotContains(response, "ray")

    def test_cook_create_get_context_data_receives_page_number(self):
        response = self.client.get(
            reverse("kitchen:cook-create"), 
            {"page": 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "dennie")
        self.assertEqual(int(response.context["page"]), 2)

    def test_toggle_assign_cook_to_existing_dish(self):
        self.user.dishes.add(self.pizza)
        self.client.get(reverse(
            "kitchen:toggle-dish-assign", 
            args=[self.pizza.pk])
        )

        self.assertNotIn(self.pizza, self.user.dishes.all())

    def test_toggle_assign_cook_to_new_dish(self):
        self.client.get(reverse(
            "kitchen:toggle-dish-assign", 
            args=[self.pizza.pk])
        )
        self.assertIn(self.pizza, self.user.dishes.all())
