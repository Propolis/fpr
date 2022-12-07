from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    RecipeIngredient
)

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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        read_only=False,
        many=True,
        required = False
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        read_only=False,
        many=True
    )

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited': bool,
            # 'is_in_shopping_cart': bool,
            'name',
            'image',    # Картинка закодирована в base64 (см. ЯП)
            'text',
            'cooking_time',
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        if tags:
            for tag in tags:
                current_tag, created = Tag.objects.get_or_create(**tag)
                recipe.tags.add(current_tag)

        return recipe
