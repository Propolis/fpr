import csv

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, TagFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CreateOrUpdateRecipeSerializer,
    IngredientSerializer,
    ReadOnlyRecipeSerializer,
    ShortReadOnlyRecipeSerializer,
    SubscribeSerializer,
    SubscriptionSerializer,
    TagSerializer
)
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag
)
from users.models import Subscription

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly | IsAdminUser]
    pagination_class = CustomPagination
    filterset_class = TagFilter
    filter_backends = [DjangoFilterBackend, ]

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
            headers={
                'Content-Disposition': 'attachment; '
                + 'filename="shopping_list.csv"'
            },
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
            return self.add_recipe(FavoriteRecipe, pk=pk)
        else:
            return self.remove_recipe(FavoriteRecipe, pk=pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, pk=pk)
        else:
            return self.remove_recipe(ShoppingCart, pk=pk)

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

    def add_recipe(self, ThroughModel, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if ThroughModel.objects.filter(recipe=recipe, user=user).exists():
            return Response(
                data={'errors': 'Рецепт уже добавлен!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ThroughModel.objects.create(recipe=recipe, user=user)
        serializer = ShortReadOnlyRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def remove_recipe(self, ThroughModel, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        object = ThroughModel.objects.filter(
            recipe=recipe,
            user=user
        )
        if not object.exists():
            return Response(
                data={
                    'errors': 'Нельзя удалить рецепт, '
                    + 'так как он не был добавлен'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListOnlySubscriptionAPIView(ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return user.subscribers.all()


class SubscribeView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        subscriber = self.request.user
        if author == subscriber:
            return Response(
                data={'errors': 'Нельзя подписаться на самого себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(
            author=author,
            subscriber=subscriber
        ).exists():
            return Response(
                data={'errors': 'Вы уже подписаны на этого пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SubscribeSerializer(
            data={
                'author': author.pk,
                'subscriber': subscriber.pk
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        subscriber = self.request.user
        if author == subscriber:
            return Response(
                data={'errors': 'Нельзя отписаться от самого себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscripton = Subscription.objects.filter(
            author=author,
            subscriber=subscriber
        )
        if not subscripton.exists():
            return Response(
                data={'errors': 'Вы не были подписаны на этого пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscripton.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
