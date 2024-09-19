from typing import Any
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import QuerySet

from .models import Dish, Cook, DishType, Ingredient
from .forms import (
    CookCreationForm,
    CookUpdateForm,
    DishForm,
    CookSearchForm,
    DishSearchForm,
    DishTypeSearchForm,
    IngredientSearchForm
)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    Handles HTTP requests to the index page,
    displaying the three most recently updated dishes.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A rendered HTML response containing
        the index page with the dishes.
    """
    dishes = Dish.objects.all().order_by("-updated_at")[:3] \
        .prefetch_related("ingredients")
    return render(request, "kitchen/index.html", {"dishes": dishes})


@login_required
def custom_logout_view(request: HttpRequest) -> HttpResponse:
    """
    Handles HTTP POST requests to log out the current user and
    redirects them to the login page.
    If the request is not a POST, it renders the logged out page.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A redirect response to the login page
        if the request is a POST, otherwise a rendered HTML response
        containing the logged out page.
    """
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request, "registration/logged_out.html")


class CookListView(LoginRequiredMixin, generic.ListView):
    template_name = "kitchen/all_cooks.html"
    model = Cook
    context_object_name = "cooks"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[Any]:
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self) -> QuerySet[Cook]:
        queryset = get_user_model().objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "kitchen/cook_detail.html"
    model = Cook
    context_object_name = "cook"


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    template_name = "kitchen/cook_form.html"
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cooks-page")

    def get_context_data(self, **kwargs) -> dict[Any]:
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
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[Any]:
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self) -> QuerySet[Dish]:
        queryset = Dish.objects.all().prefetch_related("ingredients")
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


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


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_types"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[Any]:
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self) -> QuerySet[DishType]:
        queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-types-page")
    context_object_name = "dish_type"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-types-page")
    context_object_name = "dish_type"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-types-page")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    template_name = "kitchen/ingredient_list.html"
    context_object_name = "ingredients"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[Any]:
        context = super(IngredientListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self) -> QuerySet[Ingredient]:
        queryset = Ingredient.objects.all()
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    template_name = "kitchen/ingredient_form.html"
    success_url = reverse_lazy("kitchen:ingredients-page")
    context_object_name = "ingredient"


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    template_name = "kitchen/ingredient_form.html"
    success_url = reverse_lazy("kitchen:ingredients-page")
    context_object_name = "ingredient"


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = "kitchen/ingredient_confirm_delete.html"
    success_url = reverse_lazy("kitchen:ingredients-page")


@login_required
def toggle_assign_to_dish(
    request: HttpRequest,
    pk: int
) -> HttpResponseRedirect:
    cook = get_user_model().objects.get(id=request.user.id)
    if Dish.objects.get(id=pk) in cook.dishes.all():
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(
        reverse_lazy(
            "kitchen:dish-detail-page",
            args=[pk]
        )
    )
