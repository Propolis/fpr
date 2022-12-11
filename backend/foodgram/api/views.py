from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CreateOrUpdateRecipeSerializer,
    IngredientSerializer,
    TagSerializer,
    ReadOnlyRecipeSerializer,
    UserSerializer,
)

User = get_user_model()


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
            'create': CreateOrUpdateRecipeSerializer,
            'update': CreateOrUpdateRecipeSerializer,
            'partial_update': CreateOrUpdateRecipeSerializer
        }
        return ACTION_SERIALIZER_CLASS.get(self.action)

    def perform_create(self, serializer):
        author = User.objects.get(id=1)
        # author = self.request.user
        serializer.save(author=author)

    def perform_update(self, serializer):
        author = User.objects.get(id=1)
        # author = self.request.user
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
