from django.contrib import admin
from .models import Category, Flower

admin.site.register(Flower)
admin.site.register(Category)