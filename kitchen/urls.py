from django.urls import path

from kitchen import views

urlpatterns = [
    path("", views.index, name="main-page"),
    path("cooks/", views.CookListView.as_view(), name="cooks-page"),
    path("cooks/<slug:slug>", views.CookDetailView.as_view(), name="cook-detail-page"),
    path("cooks/create/", views.CookCreateView.as_view(), name="cook-create"),
]

app_name="kitchen"
