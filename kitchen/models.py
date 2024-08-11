from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
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
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    profile_picture = models.ImageField(
        upload_to="profile_images", 
        blank=True, 
        null=True
    )

    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.username}: ({self.first_name} {self.last_name})"


class Ingredient(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[DecimalValidator]
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
        through="DishIngredient",
        related_name="dishes"
    )
    image = models.ImageField(upload_to="dish_images", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=20)

    # constraint to ensure that each ingredient can only appear once per dish
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["dish", "ingredient"], name="unique_dish_ingredient")
        ]

    def __str__(self) -> str:
        return f"{self.dish.name} - {self.ingredient.name}: {self.quantity} {self.unit}"
