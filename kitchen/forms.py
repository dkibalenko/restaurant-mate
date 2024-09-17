from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator

from .models import Cook, Dish, Ingredient


def profile_picture_extension_validator():
    """
    Returns a forms.ImageField instance with a validator that checks if the
    uploaded file has a valid image extension.

    The allowed extensions are: .jpg, .png, .jpeg.

    The field is not required and uses a forms.FileInput widget.

    Returns:
        forms.ImageField: A forms.ImageField instance with the specified
        validator and widget.
    """
    profile_picture = forms.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "png", "jpeg"]
            )
        ],
        widget=forms.FileInput
    )

    return profile_picture


class CookCreationForm(UserCreationForm):
    profile_picture = profile_picture_extension_validator()

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "profile_picture",
        )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class CookUpdateForm(forms.ModelForm):
    profile_picture = profile_picture_extension_validator()

    class Meta:
        model = Cook
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "profile_picture",
            "bio",
        )


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        exclude = ("created_at", "updated_at",)


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        )
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )
