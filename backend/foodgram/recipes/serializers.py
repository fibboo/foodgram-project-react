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


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeCreateUpdateDestroySerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
    )
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )
        model = Recipe

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data, author=self.context['request'].user
        )

        for tag in tags:
            current_tag = get_object_or_404(Tag, pk=tag.id)
            TagRecipe.objects.create(tag=current_tag, recipe=recipe)

        for ingredient in ingredients:
            IngredientRecipe.objects.get_or_create(
                ingredient=ingredient['id'], recipe=recipe,
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

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            return Favorite.objects.filter(
                user=self.context['request'].user, recipe=obj
            ).exists()

        return None

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            shopping_cart = ShoppingCart.objects.get_or_create(
                user=self.context['request'].user,
            )
            return ShoppingCartRecipe.objects.filter(
                shopping_cart=shopping_cart[0], recipe=obj
            ).exists()

        return None
