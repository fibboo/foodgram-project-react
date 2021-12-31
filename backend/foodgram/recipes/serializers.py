from rest_framework import serializers

from users.models import Favorite, ShoppingCartRecipe, ShoppingCart
from users.serializers import CustomUserSerializer
from recipes.models import Recipe, Tag, Ingredient


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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart =serializers.SerializerMethodField()

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
