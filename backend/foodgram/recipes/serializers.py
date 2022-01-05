from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import Favorite, ShoppingCartRecipe, ShoppingCart
from users.serializers import CustomUserSerializer
from recipes.models import Recipe, Tag, Ingredient, TagRecipe, IngredientRecipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeCreateUpdateDestroySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )
        model = Recipe

    def validate_tags(self, value):
        for i in value:
            if Tag.objects.filter(pk=i).first() is None:
                raise serializers.ValidationError('Tag not found')

    def create(self, validated_data):
        print(validated_data)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            current_tag = get_object_or_404(Tag, pk=tag)
            TagRecipe.objects.create(tag=current_tag, recipe=recipe)

        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, pk=ingredient['id'],
            )
            IngredientRecipe.objects.create(
                ingredient=current_ingredient, recipe=recipe,
                amount=ingredient['amount'],
            )

        return recipe


class RecipeListRetrieveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        )
        model = Recipe

    # to-do don't like implementation. Rewrite
    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            favorite = Favorite.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).first()
        else:
            favorite = None
        return favorite is not None

    # to-do don't like implementation. Rewrite
    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            shopping_cart = ShoppingCart.objects.get_or_create(
                user=self.context['request'].user,
            )
            shopping_cart_recipe = ShoppingCartRecipe.objects.filter(
                shopping_cart=shopping_cart[0],
                recipe=obj
            ).first()
        else:
            shopping_cart_recipe = None
        return shopping_cart_recipe is not None
