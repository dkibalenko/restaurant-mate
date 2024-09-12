from freezegun import freeze_time
from urllib.parse import urlparse, parse_qs
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Ingredient, Dish

MAIN_PAGE_URL = reverse("kitchen:main-page")


class PublicViewTest(TestCase):
    def test_index_login_required_and_redirect_to_login_page(self):
        response = self.client.get(MAIN_PAGE_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=%2F")

    def test_cook_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("kitchen:cooks-page"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fcooks%2F"
        )

    def test_dish_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("kitchen:dishes-page"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fdishes%2F"
        )

    def test_dish_type_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("kitchen:dish-types-page"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fdish_types%2F"
        )
    
    def test_ingredient_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("kitchen:ingredients-page"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fingredients%2F"
        )


class CustomLogoutViewTest(TestCase):
    def setUp(self):
        self.cook = get_user_model().objects.create_user(
            username="dennie",
            password="testpassword"
        )
        self.client.login(username="dennie", password="testpassword")

    def test_get_logout_view(self):
        response  = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/logged_out.html")

    def test_post_logout_view(self):
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_user_is_logged_out(self):
        self.client.post(reverse("logout"))
        response = self.client.get(MAIN_PAGE_URL)
        expected_redirect_url = (
            f"{reverse('login')}?"
            f"next=/{MAIN_PAGE_URL}/"
        )

        parsed_response_url = urlparse(response.url)
        parsed_expected_redirect_url = urlparse(expected_redirect_url)

        self.assertEqual(
            parsed_response_url.path, 
            parsed_expected_redirect_url.path
        )

        response_next_parameter = (
            parse_qs(parsed_response_url.query).get("next", [""])[0]
            .rstrip("/")
        )
        expected_redirect_url_next_parameter = (
            parse_qs(parsed_expected_redirect_url.query).get("next", [""])[0]
            .rstrip("/")
        )

        self.assertEqual(
            response_next_parameter, 
            expected_redirect_url_next_parameter
        )

class PrivateViewTest(TestCase):
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

        self.dish_data = [
            {
                "name": "Pizza",
                "description": "Pizza description",
                "price": 10.00,
                "image": "pizza.png",
                "freeze_time_str": "2024-09-10",
                "ingredients": [self.ingredient1, self.ingredient2]
            },
            {
                "name": "Pasta",
                "description": "Pasta description",
                "price": 9.00,
                "image": "pasta.png",
                "freeze_time_str": "2024-09-09",
                "ingredients": [self.ingredient1]
            },
            {
                "name": "Salad",
                "description": "Salad description",
                "price": 8.00,
                "image": "salad.png",
                "freeze_time_str": "2024-09-08",
                "ingredients": [self.ingredient2]
            },
            {
                "name": "Soup",
                "description": "Soup description",
                "price": 7.00,
                "image": "soup.png",
                "freeze_time_str": "2024-09-07",
                "ingredients": [self.ingredient1, self.ingredient2]
            }
        ]
        
        for dish_data in self.dish_data:
            with freeze_time(dish_data["freeze_time_str"]):
                dish = Dish.objects.create(
                    name=dish_data["name"],
                    description=dish_data["description"],
                    price=dish_data["price"],
                    dish_type=self.dish_type,
                    image=dish_data["image"]
                )
                dish.ingredients.add(*dish_data["ingredients"])

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
