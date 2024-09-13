from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType, Ingredient
from kitchen.forms import CookSearchForm

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

        get_user_model().objects.create_user(
            username="john",
            first_name="John",
            last_name="Wick",
            profile_picture="john.jpg",
            password="testjohnwick"
        )
        get_user_model().objects.create_user(
            username="ray",
            first_name="Ray",
            last_name="Charles",
            profile_picture="ray.jpg",
            password="testraycharles"
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
        ]

        for dish_data in cls.dish_data:
            dish = Dish.objects.create(
                name=dish_data["name"],
                description=dish_data["description"],
                price=dish_data["price"],
                dish_type=cls.dish_type,
                image=dish_data["image"]
            )
            dish.ingredients.add(*dish_data["ingredients"])

        cls.pizza = Dish.objects.get(name="Pizza")
        cls.client.force_login(cls.user)

    def test_cook_get_context_data_receives_correct_search_form(self):
        response = self.client.get(COOKS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], CookSearchForm)

    def test_cook_get_queryset_with_valid_search_form(self):
        response = self.client.get(COOKS_LIST_URL, {"username": "dennie"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "dennie")
        self.assertNotContains(response, "ray")

    def test_cook_get_queryset_with_invalid_search_form(self):
        response = self.client.get(COOKS_LIST_URL, {"username": 123})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "john")
        self.assertNotContains(response, "ray")

    def test_cook_create_get_context_data_receives_page_number(self):
        response = self.client.get(
            reverse("kitchen:cook-create"), 
            {"page": 3}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "dennie")
        self.assertEqual(int(response.context["page"]), 3)

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
