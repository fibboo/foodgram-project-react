from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Recipe, Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientSerializer(many=True)

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients',
            # 'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        )
        model = Recipe
