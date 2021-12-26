from rest_framework import serializers

from .models import Recipe, Tag, Ingredient


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient
