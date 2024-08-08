from django.urls import path

from kitchen.views import index

urlpatterns = [
    path("", index, name="main-page")
]

app_name="kitchen"
