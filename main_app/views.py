from django.shortcuts import render
from django.http import HttpResponse


# create your views here
# controller code in python
# we call theses view funcitons
def home(request):
    # each view receives a request object
    return HttpResponse("<h1>Hello ᓚᘏᗢ</h1>")
    # we return an HttpResponse object to respond


def about(request):
    return render(request, "about.html")  # same thing as res.render


# views.py


class Cat:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age


# Create a list of Cat instances
cats = [
    Cat("Lolo", "tabby", "Kinda rude.", 3),
    Cat("Sachi", "tortoiseshell", "Looks like a turtle.", 0),
    Cat("Fancy", "bombay", "Happy fluff ball.", 4),
    Cat("Bonk", "selkirk rex", "Meows loudly.", 6),
]

# views.py


def cat_index(request):
    # Render the cats/index.html template with the cats data
    return render(request, "cats/index.html", {"cats": cats})
