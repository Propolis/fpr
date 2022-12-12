from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    Tag,
)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from .serializers import (
    CreateOrUpdateRecipeSerializer,
    IngredientSerializer,
    TagSerializer,
    ReadOnlyRecipeSerializer,
    ShortRecipeSerializer
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

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, pk=pk)
            user = request.user
            if FavoriteRecipe.objects.filter(recipe=recipe, user=user).exists():
                raise ValidationError('Уже в избранном!')
            FavoriteRecipe.objects.create(recipe=recipe, user=user)
            serializer = ShortRecipeSerializer(recipe)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        favorite = FavoriteRecipe.objects.filter(recipe=recipe, user=user)
        if not favorite.exists():
            raise ValidationError('Рецепт не был в избранном!')
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def perform_update(self, serializer):
        author = self.request.user
        serializer.save(author)

