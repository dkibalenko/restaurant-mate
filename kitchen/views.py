from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView

from .models import Dish, Cook


def index(request: HttpRequest) -> HttpResponse:
    dishes = Dish.objects.all().order_by("-updated_at")[:3]
    return render(request, "kitchen/index.html", {"dishes": dishes})


class CookListView(ListView):
    template_name = "kitchen/all_cooks.html"
    model = Cook
    context_object_name = "cooks"
