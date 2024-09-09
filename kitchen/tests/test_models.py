from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Ingredient


class ModelsTests(TestCase):
    def setUp(self):
        self.cook = get_user_model().objects.create_user(
            username="testuser",
            first_name="Test_first_name",
            last_name="Test_last_name",
            password="testpassword"
        )
        self.dish_type = DishType.objects.create(name="Pizza")
        self.ingredient = Ingredient.objects.create(name="Water")
    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), self.dish_type.name)

    def test_cook_str(self):
        self.assertEqual(
            str(self.cook), 
            f"{self.cook.username}: ({self.cook.full_name()})"
        )

    def test_cook_saved_with_slug(self):
        self.assertEqual(
            self.cook.slug, 
            f"{self.cook.first_name.lower()}-{self.cook.last_name.lower()}"
        )

    def test_cook_get_absolute_url(self):
        self.assertEqual(
            self.cook.get_absolute_url(), 
            reverse(
                "kitchen:cook-detail-page", 
                kwargs={"slug": self.cook.slug}
            )
        )

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), self.ingredient.name)
