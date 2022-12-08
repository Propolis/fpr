from django.urls import include, path
from rest_framework import routers

from .views import (
    CreateRecipeSerializer,
    IngredientViewSet,
    TagViewSet,
    RecipeViewSet,
)

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
