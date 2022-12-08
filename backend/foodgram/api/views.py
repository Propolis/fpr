from django.contrib.auth import get_user_model
from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
)
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    IngredientSerializer,
    TagSerializer,
    ListRetrieveRecipeSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ListRetrieveRecipeSerializer
