from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Dish


def index(request: HttpRequest) -> HttpResponse:
    dishes = Dish.objects.all().order_by("-updated_at")[:3]
    return render(request, "kitchen/index.html", {"dishes": dishes})
