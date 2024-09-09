from django.test import TestCase
from django import setup
import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_mate.settings")
# setup()

from .models import DishType


class ModelsTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="Pizza")
        self.assertEqual(str(dish_type), dish_type.name)
