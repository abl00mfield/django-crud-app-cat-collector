from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cat


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
    return render(request, "cats/detail.html", {"cat": cat})


class CatCreate(CreateView):
    model = Cat
    fields = ["name", "breed", "description", "age"]


class CatUpdate(UpdateView):
    model = Cat
    fields = ["breed", "description", "age"]


class CatDelete(DeleteView):
    model = Cat
    success_url = "/cats/"
