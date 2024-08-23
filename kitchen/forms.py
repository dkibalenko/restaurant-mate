from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator

from .models import Cook


class CookCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "png", "jpeg"]
            )
        ],
        widget=forms.FileInput
    )
    
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "profile_picture",
        )
