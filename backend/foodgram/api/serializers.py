from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (
    Tag,
    Recipe,
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
            # 'is_subscribed',
        ]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']
        read_only_fields = ['__all__']


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many = False, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited' -> bool,
            # 'is_in_shopping_cart' -> bool,
            'name',
            'image',    # Преобразовывать картинки в base64 (см. ЯП)
            'text',
            'cooking_time',
        ]
