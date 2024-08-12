from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Cook, DishType, Dish, Ingredient, DishIngredient


class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1  # Number of extra forms to display


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "dish_type", "price", "created_at", "updated_at",)
    inlines = [DishIngredientInline]


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description",)


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("bio", "years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("bio", "years_of_experience", "profile_picture",)}),)  # for fields to be used in editing users
    )
    add_fieldsets = UserAdmin.add_fieldsets + (  # for fields to be used when creating a user
        (
            (
                "Additional info",
                {
                    "fields": (
                        "bio",
                        "years_of_experience"
                    )
                },
            ),
        )
    )
    search_fields = ("username", "first_name", "last_name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
