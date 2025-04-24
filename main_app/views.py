from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy
from .forms import FeedingForm


# create your views here
# controller code in python
# we call theses view funcitons
def home(request):
    # each view receives a request object
    return render(request, "home.html")


# we return an HttpResponse object to respond


def about(request):
    contact_details = "contact us at help@gmail.com"
    return render(
        request, "about.html", {"contact": contact_details}
    )  # same thing as res.render


# views.py


def cat_index(request):
    # Render the cats/index.html template with the cats data
    cats = Cat.objects.all()
    return render(request, "cats/index.html", {"cats": cats})


def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list("id"))
    toys = Toy.objects.all()  # fetch all toys
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


class CatCreate(CreateView):
    model = Cat
    fields = ["name", "breed", "description", "age"]


class CatUpdate(UpdateView):
    model = Cat
    fields = ["breed", "description", "age"]


class CatDelete(DeleteView):
    model = Cat
    success_url = "/cats/"


def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect("cat-detail", cat_id=cat_id)


class ToyCreate(CreateView):
    model = Toy
    fields = ["name", "color"]


class ToyList(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy


class ToyUpdate(UpdateView):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(DeleteView):
    model = Toy
    success_url = "/toys/"


def associate_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect("cat-detail", cat_id=cat_id)
