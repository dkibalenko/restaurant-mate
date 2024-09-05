from django.urls import path

from kitchen import views

urlpatterns = [
    path("", views.index, name="main-page"),
    path("cooks/", views.CookListView.as_view(), name="cooks-page"),
    path("cooks/<slug:slug>", views.CookDetailView.as_view(), name="cook-detail-page"),
    path("cooks/create/", views.CookCreateView.as_view(), name="cook-create"),
    path("cooks/<slug:slug>/update/", views.CookUpdateView.as_view(), name="cook-update"),
    path("cooks/<slug:slug>/delete/", views.CookDeleteView.as_view(), name="cook-delete"),
    path("dishes/", views.DishListView.as_view(), name="dishes-page"),
    path("dishes/<int:pk>/", views.DishDetailView.as_view(), name="dish-detail-page"),
    path("dishes/create/", views.DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/update/", views.DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", views.DishDeleteView.as_view(), name="dish-delete"),
    path("dishes/<int:pk>/assign/", views.toggle_assign_to_dish, name="toggle-dish-assign"),
    path("dish_types/", views.DishTypeListView.as_view(), name="dish-types-page"),
    path("dish_types/create", views.DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish_types/<int:pk>/update", views.DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish_types/<int:pk>/delete", views.DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("ingredients/", views.IngredientListView.as_view(), name="ingredients-page"),
]

app_name="kitchen"
