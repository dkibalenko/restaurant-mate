from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.paginator import Paginator

from kitchen.models import Dish, DishType, Ingredient
from kitchen.forms import DishSearchForm
from .db_test_data import dish_data


DISHES_LIST_URL = reverse("kitchen:dishes-page")


class PrivateDishViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="dennie",
            first_name="Dennie",
            last_name="Denniston",
            profile_picture="dennie.jpg",
            password="testpassword"
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


    def setUp(self) -> None:
        self.client.force_login(self.user)

        self.dishes_page_1 = self.client.get(DISHES_LIST_URL)
        self.dishes_page_2 = self.client.get(DISHES_LIST_URL, {"page": 2})
        self.all_dishes = Dish.objects.all()

    def test_retrieve_dishes_per_paginated_page(self):
        self.assertEqual(self.dishes_page_1.status_code, 200)
        self.assertEqual(len(self.dishes_page_1.context["dishes"]), 6)

        self.assertEqual(self.dishes_page_2.status_code, 200)
        self.assertEqual(len(self.dishes_page_2.context["dishes"]), 1)

        self.assertEqual(self.all_dishes.count(), 7)
        self.assertEqual(
            list(self.all_dishes),
            list(self.dishes_page_1.context["dishes"]) +
            list(self.dishes_page_2.context["dishes"])
        )
        self.assertTemplateUsed(self.dishes_page_1, "kitchen/dishes_list.html")

    def test_dish_list_contains_correct_dishes_per_paginated_page(self):
        first_page_6_dishes = self.all_dishes[:6]
        last_page_1_dish = self.all_dishes[6]
        
        self.assertEqual(self.dishes_page_1.status_code, 200)
        for dish in first_page_6_dishes:
            self.assertContains(self.dishes_page_1, dish.name)
        self.assertNotContains(self.dishes_page_1, last_page_1_dish.name)

        self.assertEqual(self.dishes_page_2.status_code, 200)
        self.assertContains(self.dishes_page_2, last_page_1_dish.name)
        for dish in first_page_6_dishes:
            self.assertNotContains(self.dishes_page_2, dish.name)

        self.assertIsInstance(
            self.dishes_page_1.context["paginator"],
            Paginator
        )
        self.assertEqual(
            str(self.dishes_page_1.context["page_obj"]),
            "<Page 1 of 2>"
        )
        self.assertTrue(self.dishes_page_1.context["is_paginated"])

    def test_dish_get_context_data_receives_correct_searchform(self):
        response = self.client.get(DISHES_LIST_URL)
        self.assertIsInstance(response.context["search_form"], DishSearchForm)

    def test_dish_get_queryset_with_valid_search_form(self):
        response = self.client.get(DISHES_LIST_URL, {"name": "Pasta"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")
        self.assertNotContains(response, "Pizza")

    def test_dish_get_queryset_with_invalid_search_form(self):
        response = self.client.get(DISHES_LIST_URL, {"name": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Pizza")
        self.assertNotContains(response, "Pasta")
        self.assertContains(response, "invalid")

    def test_dish_get_queryset_with_no_search_form_data(self):
        self.assertEqual(
            list(self.all_dishes),
            list(self.dishes_page_1.context["dishes"]) +
            list(self.dishes_page_2.context["dishes"])
        )
