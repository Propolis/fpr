from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    RecipeIngredient,
    RecipeTag
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


class ReadOnlyRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    # amount = serializers.IntegerField(source='recipeingredient_set')
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        read_only=False
    )
    # amount = serializers.PrimaryKeyRelatedField(queryset=Ingredient.recipes)
    # id = serializers.ModelField(model_field=Ingredient)

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

    class Meta:
        read_only_fields = ['__all__']
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


class CreateRecipeSerializer(serializers.ModelSerializer):
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
