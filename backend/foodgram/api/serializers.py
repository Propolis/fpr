from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Tag,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
)
from users.models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed:bool',
        ]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']
        read_only_fields = ['__all__']


class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class ReadOnlyRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        read_only=False
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']


class RecipeTagSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='tag.id')

    class Meta:
        model = RecipeTag


class ReadOnlyRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(many=False)
    ingredients = ReadOnlyRecipeIngredientSerializer(many=True, source='recipeingredient_set')
    is_favorited = serializers.SerializerMethodField(method_name='check_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(method_name='check_is_in_shopping_cart')

    def is_in_list(self, obj, model):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return model.objects.filter(user=request.user, recipe=obj).exists()

    def check_is_favorited(self, recipe):
        return self.is_in_list(recipe, FavoriteRecipe)

    def check_is_in_shopping_cart(self, recipe):
        return self.is_in_list(recipe, ShoppingCart)

    class Meta:
        read_only_fields = ['__all__']
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',    # Картинка закодирована в base64 (см. ЯП)
            'text',
            'cooking_time',
        ]


class CreateOrUpdateRecipeSerializer(serializers.ModelSerializer):
    ingredients = CreateRecipeIngredientSerializer(
        read_only=False,
        many=True,
        required=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        read_only=False,
        many=True,
        required=False
    )

    class Meta:
        depth = 3
        model = Recipe
        fields = [
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        ]

    def to_representation(self, recipe):
        serializer = ReadOnlyRecipeSerializer(recipe, context=self.context)
        return serializer.data


    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags', None)
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            amount = ingredient.get('amount')
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_id,
                amount=amount
            )
        if tags:
            for tag in tags:
                RecipeTag.objects.create(recipe=recipe, tag=tag)
        return recipe


    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        if ingredients:
            recipe.ingredients.clear()
            for ingredient in ingredients:
                ingredient_id = ingredient.get('id')
                amount = ingredient.get('amount')
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient_id,
                    amount=amount
                )
        if tags:
            recipe.tags.clear()
            for tag in tags:
                RecipeTag.objects.create(recipe=recipe, tag=tag)
        return recipe


class ShortReadOnlyRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time'
        ]

class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(
        method_name='check_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='count_recipes'
    )

    def check_is_subscribed(self, subscription):
        current_user = self.context.get('request').user
        return Subscription.objects.filter(
            author=subscription.author,
            subscriber=current_user
        ).exists()

    def get_recipes(self, subscription):
        queryset = Recipe.objects.filter(author=subscription.author)
        serializer = ShortReadOnlyRecipeSerializer(
            queryset,
            read_only=True,
            many=True
        )
        return serializer.data

    def count_recipes(self, subscription):
        return Recipe.objects.filter(author=subscription.author).count()


    class Meta:
        model = Subscription
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]


class SubscribeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = SubscriptionSerializer(
            instance,
            context=context
        )
        return serializer.data
    
    class Meta:
        model = Subscription
        fields = '__all__'
