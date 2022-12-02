from django.contrib import admin
from .models import Ingridient, Recipe, Tag


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
