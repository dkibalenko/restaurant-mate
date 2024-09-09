from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import DishType


class ModelsTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="Pizza")
        self.assertEqual(str(dish_type), dish_type.name)

    def test_cook_str(self):
        cook = get_user_model().objects.create(
            username="testuser",
            first_name="Test_first_name",
            last_name="Test_last_name",
            password="testpassword"
        )
        self.assertEqual(
            str(cook), 
            f"{cook.username}: ({cook.full_name()})"
        )

    def test_cook_saved_with_slug(self):
        cook = get_user_model().objects.create(
            username="testuser", 
            first_name="Test_first_name", 
            last_name="Test_last_name", 
            password="testpassword"
        )
        self.assertEqual(
            cook.slug, 
            f"{cook.first_name.lower()}-{cook.last_name.lower()}"
        )

    def test_get_absolute_url(self):
        cook = get_user_model().objects.create(
            username="testuser", 
            first_name="Test_first_name", 
            last_name="Test_last_name", 
            password="testpassword"
        )
        self.assertEqual(
            cook.get_absolute_url(), 
            reverse(
                "kitchen:cook-detail-page", 
                kwargs={"slug": cook.slug}
            )
        )
