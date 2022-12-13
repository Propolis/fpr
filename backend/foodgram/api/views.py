import csv
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from .serializers import (
    CreateOrUpdateRecipeSerializer,
    IngredientSerializer,
    ReadOnlyRecipeSerializer,
    ShortReadOnlyRecipeSerializer,
    TagSerializer,
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

    def create_csv_file(self, ingredients):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="shopping_list.csv"'},
            status=status.HTTP_201_CREATED
        )
        ingredients = list(ingredients)

        writer = csv.DictWriter(
            response,
            fieldnames=[
                'ingredient__name',
                'ingredient__measurement_unit',
                'ingredient_total'
            ],
        )
        for row in ingredients:
            writer.writerow(row)
        return response

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
            serializer = ShortReadOnlyRecipeSerializer(recipe)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        favorite = FavoriteRecipe.objects.filter(recipe=recipe, user=user)
        if not favorite.exists():
            raise ValidationError('Рецепт не был в избранном!')
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, pk=pk)
            user = request.user
            if ShoppingCart.objects.filter(recipe=recipe, user=user).exists():
                raise ValidationError('Уже в корзине!')
            ShoppingCart.objects.create(recipe=recipe, user=user)
            serializer = ShortReadOnlyRecipeSerializer(recipe)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            recipe = get_object_or_404(Recipe, pk=pk)
            user = request.user
            shopping_cart = ShoppingCart.objects.filter(recipe=recipe, user=user)
            if not shopping_cart.exists():
                raise ValidationError('Рецепт не был в корзине!')
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get', ],
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart_recipes__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(
            ingredient_total=Sum('amount')
        )
        return self.create_csv_file(ingredients)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def perform_update(self, serializer):
        author = self.request.user
        serializer.save(author)

