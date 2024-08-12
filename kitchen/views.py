from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Cook


def index(request: HttpRequest) -> HttpResponse:
    cooks = Cook.objects.all()
    return render(request, "kitchen/index.html", {"cooks": cooks})
