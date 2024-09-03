from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.urls import reverse_lazy


from .models import Dish, Cook
from .forms import CookCreationForm, CookUpdateForm, DishForm


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


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    template_name = "kitchen/cook_form.html"
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cooks-page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = self.request.GET.get("page", 1)
        return context


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    template_name = "kitchen/cook_form.html"
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-detail-page")
    context_object_name = "cook"


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "kitchen/cook_confirm_delete.html"
    success_url = reverse_lazy("kitchen:cooks-page")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "kitchen/dishes_list.html"
    context_object_name = "dishes"
    paginate_by = 3


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    context_object_name = "dish"


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen:dishes-page")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dishes-page")
    context_object_name = "dish"


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dishes-page")
