from django.contrib import admin
from .models import Category, Dog, Ingredient


admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Dog)