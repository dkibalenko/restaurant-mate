from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Cook, DishType, Dish, Ingredient


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "dish_type", "price", "created_at", "updated_at",)


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description",)


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("bio", "years_of_experience",)
    # to be used in editing users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'slug')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('bio', 'years_of_experience', 'profile_picture')}),
    )
    # to be used when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'slug'),
        }),
        ('Additional info', {
            'fields': ('bio', 'years_of_experience', 'profile_picture'),
        }),
    )
    search_fields = ("username", "first_name", "last_name",)
    readonly_fields = ("slug",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
