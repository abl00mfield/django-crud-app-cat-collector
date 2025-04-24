from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cat, Toy
from .forms import FeedingForm

# create your views here
# controller code in python
# we call theses view funcitons


class Home(LoginView):
    template_name = "home.html"


def about(request):
    contact_details = "contact us at help@gmail.com"
    return render(
        request, "about.html", {"contact": contact_details}
    )  # same thing as res.render


@login_required
def cat_index(request):
    # Render the cats/index.html template with the cats data
    cats = Cat.objects.filter(user=request.user)
    return render(request, "cats/index.html", {"cats": cats})


@login_required
def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list("id"))

    feeding_form = FeedingForm()
    return render(
        request,
        "cats/detail.html",
        {
            "cat": cat,
            "feeding_form": feeding_form,
            "toys": toys_cat_doesnt_have,  # pass toys to the template
        },
    )


class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ["name", "breed", "description", "age"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ["breed", "description", "age"]


class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = "/cats/"


@login_required
def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect("cat-detail", cat_id=cat_id)


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ["name", "color"]


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = "/toys/"


@login_required
def associate_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect("cat-detail", cat_id=cat_id)


@login_required
def remove_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect("cat-detail", cat_id=cat_id)


def signup(request):
    error_message = ""
    if request.method == "POST":
        # create a user from an object
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # add the user to the db
            user = form.save()
            # now log them in
            login(request, user)
            return redirect("cat-index")
        else:
            error_message = "Invalid sign up - try again"
    # if the post request was bad or they sent a GET request
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "signup.html", context)
