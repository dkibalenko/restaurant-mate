from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.paginator import Paginator

from kitchen.models import Dish, DishType, Ingredient
from kitchen.forms import DishSearchForm


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
        cls.dish_data = [
            {
                "name": "Pizza",
                "description": "Pizza description",
                "price": 10.00,
                "image": "pizza.png",
                "freeze_time_str": "2024-09-10",
                "ingredients": [cls.ingredient1, cls.ingredient2]
            },
            {
                "name": "Pasta",
                "description": "Pasta description",
                "price": 9.00,
                "image": "pasta.png",
                "freeze_time_str": "2024-09-09",
                "ingredients": [cls.ingredient1]
            },
            {
                "name": "Salad",
                "description": "Salad description",
                "price": 8.00,
                "image": "salad.png",
                "freeze_time_str": "2024-09-08",
                "ingredients": [cls.ingredient2]
            },
            {
                "name": "Soup",
                "description": "Soup description",
                "price": 7.00,
                "image": "soup.png",
                "freeze_time_str": "2024-09-07",
                "ingredients": [cls.ingredient1, cls.ingredient2]
            }
        ]

        for data in cls.dish_data:
            dish = Dish.objects.create(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                dish_type=cls.dish_type,
                image=data["image"]
            )
            dish.ingredients.add(*data["ingredients"])


    def setUp(self) -> None:
        self.client.force_login(self.user)

        self.dishes_page_1 = self.client.get(DISHES_LIST_URL)
        self.dishes_page_2 = self.client.get(DISHES_LIST_URL, {"page": 2})
        self.all_dishes = Dish.objects.all()

    def test_retrieve_dishes_per_paginated_page(self):
        self.assertEqual(self.dishes_page_1.status_code, 200)
        self.assertEqual(len(self.dishes_page_1.context["dishes"]), 3)

        self.assertEqual(self.dishes_page_2.status_code, 200)
        self.assertEqual(len(self.dishes_page_2.context["dishes"]), 1)

        self.assertEqual(self.all_dishes.count(), 4)
        self.assertEqual(
            list(self.all_dishes),
            list(self.dishes_page_1.context["dishes"]) +
            list(self.dishes_page_2.context["dishes"])
        )
        self.assertTemplateUsed(self.dishes_page_1, "kitchen/dishes_list.html")

    def test_dish_list_contains_correct_dishes_per_paginated_page(self):
        response_page_1 = self.dishes_page_1
        response_page_2 = self.dishes_page_2
        self.assertEqual(response_page_1.status_code, 200)
        self.assertContains(response_page_1, "Pizza")
        self.assertContains(response_page_1,"Pasta")
        self.assertContains(response_page_1,"Salad")
        self.assertNotContains(response_page_1,"Soup")

        self.assertEqual(response_page_2.status_code, 200)
        self.assertContains(response_page_2,"Soup")
        self.assertNotContains(response_page_2,"Pizza")
        self.assertNotContains(response_page_2,"Pasta")
        self.assertNotContains(response_page_2,"Salad")

        self.assertIsInstance(
            response_page_1.context["paginator"],
            Paginator
        )
        self.assertEqual(
            str(response_page_1.context["page_obj"]),
            "<Page 1 of 2>"
        )
        self.assertTrue(response_page_1.context["is_paginated"])

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
