from django.contrib.auth import get_user_model
from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
)
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CreateRecipeSerializer,
    IngredientSerializer,
    TagSerializer,
    ReadOnlyRecipeSerializer,
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

    def get_serializer_class(self):
        ACTION_SERIALIZER_CLASS = {
            'list': ReadOnlyRecipeSerializer,
            'retrieve': ReadOnlyRecipeSerializer,
            'create': CreateRecipeSerializer,
        }
        return ACTION_SERIALIZER_CLASS.get(self.action)

    def perform_create(self, serializer):
        # author = self.request.user
        author = User.objects.get(id=1)
        serializer.save(author=author)
