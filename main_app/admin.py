from django.contrib import admin
from .models import Cat, Feeding, Toy

# Register your models here.
admin.site.register([Cat, Feeding, Toy])
