from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import generic

from .models import Dish, Cook

@login_required
def index(request: HttpRequest) -> HttpResponse:
    dishes = Dish.objects.all().order_by("-updated_at")[:3]
    return render(request, "kitchen/index.html", {"dishes": dishes})

@login_required
def custom_logout_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request, "registration/logged_out.html")


class CookListView(LoginRequiredMixin, generic.ListView):
    template_name = "kitchen/all_cooks.html"
    model = Cook
    context_object_name = "cooks"
    paginate_by = 3


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "kitchen/cook_detail.html"
    model = Cook
    context_object_name = "cook"
