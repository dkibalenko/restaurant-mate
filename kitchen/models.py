from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    DecimalValidator,
)


class DishType(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Cook(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    years_of_experience = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        default=0
    )
    profile_picture = models.ImageField(
        upload_to="profile_images",
    )
    slug = models.SlugField(unique=True, blank=True, db_index=True)

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.username}: ({self.full_name()})"

    def generate_unique_slug(self):
        """
        Generates a unique slug for the user. If the user has a first and last
        name, the slug will be based on those. Otherwise, it will be based on
        the username. The slug will be made unique by appending a number to
        the end if the generated slug is already taken.

        Returns:
        str: The unique slug
        """
        if self.first_name and self.last_name:
            base_slug = slugify(f"{self.first_name}-{self.last_name}")
        else:
            base_slug = slugify(self.username)

        slug = base_slug
        num = 1
        while get_user_model().objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1

        return slug

    def save(self, *args, **kwargs) -> None:
        """
        Saves the user and updates the slug if the first or last name changed.

        If the user is being created, the slug is generated from the first
        and last name if they exist.
        If the user is being updated and the first or last name changed,
        the slug is regenerated.
        """
        if self.pk:
            existing_cook = get_user_model().objects.get(pk=self.pk)
            if (
                self.first_name != existing_cook.first_name
                or self.last_name != existing_cook.last_name
            ):
                self.slug = self.generate_unique_slug()
        else:
            self.slug = self.generate_unique_slug()

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("kitchen:cook-detail-page", kwargs={"slug": self.slug})


class Ingredient(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[DecimalValidator(max_digits=9, decimal_places=2)]
    )
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="dishes"
    )
    image = models.ImageField(upload_to="dish_images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "dishes"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("kitchen:dish-detail-page", kwargs={"pk": self.pk})
