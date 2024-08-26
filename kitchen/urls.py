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
]

app_name="kitchen"
