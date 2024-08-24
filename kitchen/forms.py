from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator

from .models import Cook


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
        required=False,
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
