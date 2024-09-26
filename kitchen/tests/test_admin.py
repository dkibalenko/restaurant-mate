from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="adminuser",
            password="adminpassword"
        )

        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cookuser",
            first_name="Test_first",
            last_name="Test_last",
            password="testpassword",
            bio="Test_bio",
            years_of_experience=49,
            profile_picture="test_profile_image.jpg"
        )
        self.cook2 = get_user_model().objects.create_user(
            username="john",
            first_name="John",
            last_name="Wick",
        )
        self.cook3 = get_user_model().objects.create_user(
            username="ray",
            first_name="Ray",
            last_name="Charles",
        )
        self.admin_cook_list_url = reverse("admin:kitchen_cook_changelist")
        self.admin_cook_detail_url = reverse(
            "admin:kitchen_cook_change",
            args=[self.cook.pk]
        )

    def test_cook_bio_years_of_experience_listed(self):
        response = self.client.get(self.admin_cook_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cook.bio)
        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_detail_custom_fields_listed(self):
        response = self.client.get(self.admin_cook_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cook.bio)
        self.assertContains(response, self.cook.years_of_experience)
        self.assertContains(response, self.cook.profile_picture)
        self.assertContains(response, self.cook.slug)

    def test_cook_create_custom_fields_listed(self):
        url = reverse("admin:kitchen_cook_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bio")
        self.assertContains(response, "years_of_experience")
        self.assertContains(response, "profile_picture")
        self.assertContains(response, "slug")

    def test_cook_search_field(self):
        response = self.client.get(self.admin_cook_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="q"')

        search_queries = [
            self.cook.username,
            self.cook.first_name,
            self.cook.last_name
        ]
        for query in search_queries:
            search_response = self.client.get(
                self.admin_cook_list_url,
                {"q": query}
            )

            self.assertEqual(search_response.status_code, 200)
            self.assertContains(search_response, "Test_first Test_last")
            self.assertNotContains(search_response, "John Wick")
            self.assertNotContains(search_response, "Ray Charles")

    def test_cook_slug_readonly(self):
        """
        Tests that the slug field is shown as read-only in the admin site.
        """
        response = self.client.get(self.admin_cook_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cook.slug)
        self.assertContains(
            response,
            f'<div class="readonly">{self.cook.slug}</div>'
        )
        self.assertNotContains(response, 'name="slug"')
