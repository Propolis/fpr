from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    inlines = [
        RecipeIngredientInline,
        RecipeTagInline
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
