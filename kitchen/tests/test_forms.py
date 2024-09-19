from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import FileExtensionValidator

from PIL import Image
import io

from kitchen.forms import (
    CookCreationForm, 
    CookUpdateForm,
    ProfilePictureMixin
)


class TestProfilePictureMixin(TestCase):
    def setUp(self):
        img = Image.new("RGB", (1, 1))
        img.putpixel((0, 0), (255, 0, 0))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")

        self.image_content = buf.getvalue()

        self.form_data = {
            "username": "dennie",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Dennie",
            "last_name": "Denniston",
            "email": "test@example.com",
            "years_of_experience": 5,
            "bio": "test bio",
        }

    def test_profile_picture_field_in_form_with_validators(self):
        form = CookCreationForm(
            data=self.form_data,
            files=SimpleUploadedFile(
                name="test_image.jpg",
                content=self.image_content,
            )
        )
        self.assertIn("profile_picture", form.fields)
        self.assertIsInstance(
            form.fields["profile_picture"], 
            forms.ImageField
        )
        
        validators = form.fields["profile_picture"].validators
        file_extension_validator = next(
            (
                validator 
                for validator 
                in validators 
                if isinstance(validator,FileExtensionValidator)
            ),
                None
        )
        self.assertIsNotNone(
            file_extension_validator, 
            "FileExtensionValidator not found in profile_picture validators"
        )
        self.assertEqual(
            file_extension_validator.allowed_extensions, 
            ["jpg", "png", "jpeg"]
        )


    def test_profile_picture_mixin_with_valid_image_extension(self):
        valid_files = [
            SimpleUploadedFile(
                name="test_image.jpg",
                content=self.image_content,
            ),
            SimpleUploadedFile(
                name="test_image.png",
                content=self.image_content,
            ),
            SimpleUploadedFile(
                name="test_image.jpeg",
                content=self.image_content,
            ),
        ]
        
        for file in valid_files:
            form = ProfilePictureMixin(
                files={"profile_picture": file}
            )
            self.assertTrue(form.is_valid())

    def test_profile_picture_mixin_with_invalid_image_extension(self):
        invalid_files = [
            SimpleUploadedFile(
                name="test_image.gif",
                content=self.image_content,
            ),
            SimpleUploadedFile(
                name="test_image.bmp",
                content=self.image_content,
            ),
        ]
        for file in invalid_files:
            form = ProfilePictureMixin(
                files={"profile_picture": file}
            )
            self.assertFalse(form.is_valid())
            self.assertIn("profile_picture", form.errors)
            self.assertIn("extension", form.errors["profile_picture"][0])


class CookFormTest(TestCase):
    def setUp(self):
        img = Image.new("RGB", (1, 1))
        img.putpixel((0, 0), (255, 0, 0))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        self.image_content = buf.getvalue()

        self.form_data = {
            "username": "dennie",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Dennie",
            "last_name": "Denniston",
            "email": "test@example.com",
            "years_of_experience": 5,
            "bio": "test bio",
        }
        self.profile_picture = {
            "profile_picture": SimpleUploadedFile(
                name="test_image.jpeg",
                content=self.image_content,
            ),
        }
        self.form = CookCreationForm(
            data=self.form_data, 
            files=self.profile_picture
        )

        self.testing_forms = (CookCreationForm, CookUpdateForm)

    def test_create_update_forms_custom_fields_presented(self):
            for testing_form in self.testing_forms:
                form = testing_form(
                    data=self.form_data, 
                    files=self.profile_picture
                )
                if isinstance(form, CookCreationForm):
                    self.assertEqual(len(form.fields), 9)
                else:
                    self.assertEqual(len(form.fields), 7)
                self.assertIn("first_name", form.fields)
                self.assertIn("last_name", form.fields)
                self.assertIn("email", form.fields)
                self.assertIn("years_of_experience", form.fields)
                self.assertIn("profile_picture", form.fields)
                self.assertIn("bio", form.fields)

    def test_form_custom_required_fields(self):
        form = CookCreationForm(
            {
                "username": "dennie",
                "password1": "testpassword",
                "password2": "testpassword",
                "email": "test@example.com",
                "years_of_experience": 5,
            }
        )
        self.assertTrue(form.fields["first_name"].required)
        self.assertTrue(form.fields["last_name"].required)
        self.assertTrue(form.fields["profile_picture"].required)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
        self.assertIn("first_name", form.errors)
        self.assertIn("last_name", form.errors)
        self.assertIn("profile_picture", form.errors)

    def test_form_with_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_form_with_invalid_password(self):
        invalid_form_data = {
            "username": "dennie",
            "password1": "testpassword",
            "password2": "invalidpassword",
            "first_name": "Dennie",
            "last_name": "Denniston",
            "years_of_experience": 5,
        }
        form = CookCreationForm(
            data=invalid_form_data, 
            files=self.profile_picture
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn("password2", form.errors)

    def test_form_with_invalid_profile_picture_extension(self):
        invalid_file = SimpleUploadedFile(
                name="test_image.gif",
                content=self.image_content,
            )
        form = CookCreationForm(
            data=self.form_data, 
            files={"profile_picture": invalid_file}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn("profile_picture", form.errors)

    def test_form_with_no_profile_picture(self):
        form = CookCreationForm(
            data=self.form_data
        )
        self.assertFalse(form.is_valid())
        self.assertIn("profile_picture", form.errors)

    def test_form_save(self):
        cook = self.form.save()
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(cook.username, "dennie")
        self.assertEqual(cook.first_name, "Dennie")
        self.assertEqual(cook.last_name, "Denniston")
        self.assertEqual(cook.email, "test@example.com")
        self.assertEqual(cook.years_of_experience, 5)
