from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
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

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.username}: ({self.first_name} {self.last_name})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)


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

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("kitchen:dish-detail-page", kwargs={"pk": self.pk})
