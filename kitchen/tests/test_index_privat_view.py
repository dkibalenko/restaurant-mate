from freezegun import freeze_time
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Ingredient, Dish
from .db_test_data import dish_data


MAIN_PAGE_URL = reverse("kitchen:main-page")


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="dennie",
            password="testpassword"
        )
        self.client.login(username="dennie", password="testpassword")

        self.dish_type = DishType.objects.create(
            name="Main Course", 
            description="Main course dishes"
        )
        
        self.ingredient1 = Ingredient.objects.create(
            name="Tomato", 
            description="Fresh tomato"
        )
        self.ingredient2 = Ingredient.objects.create(
            name="Cheese", 
            description="Cheddar cheese"
        )
        
        for data in dish_data:
            with freeze_time(data["freeze_time_str"]):
                dish = Dish.objects.create(
                    name=data["name"],
                    description=data["description"],
                    price=data["price"],
                    dish_type=self.dish_type,
                    image=data["image"]
                )
                dish.ingredients.add(self.ingredient1, self.ingredient2)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/index.html")

    def test_index_view_contains_three_last_updated_dishes(self):
        response = self.client.get(MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza")
        self.assertContains(response, "Pasta")
        self.assertContains(response, "Salad")
        self.assertNotContains(response, "Soup")

    def test_index_displays_three_last_updated_dishes(self):
        response = self.client.get(MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)

        dishes = response.context["dishes"]
        self.assertEqual(len(dishes), 3)
        self.assertEqual(dishes[0].name, "Pizza")
        self.assertEqual(dishes[1].name, "Pasta")
        self.assertEqual(dishes[2].name, "Salad")
