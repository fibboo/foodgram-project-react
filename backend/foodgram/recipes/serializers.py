from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer, RecipeSerializer
from .models import Recipe, Tag, Ingredient, IngredientRecipe

User = get_user_model()


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
    amount = serializers.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeCreateUpdateDestroySerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
    )
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )
        model = Recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListRetrieveSerializer(instance, context=context).data

    def empty_unique_validator(self, lst, field_name):
        if not lst:
            raise serializers.ValidationError(
                {field_name: 'Must be at least one'}
            )
        check_list = []
        for tag in lst:
            if tag in check_list:
                raise serializers.ValidationError(
                    {field_name: f'{field_name} must be unique'}
                )
            check_list.append(tag)

    def validate(self, data):
        tags = data.get('tags')
        self.empty_unique_validator(tags, 'tags')
        ingredients = data.get('ingredients')
        self.empty_unique_validator(ingredients, 'ingredients')
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data, author=self.context['request'].user
        )

        for tag in tags:
            current_tag = get_object_or_404(Tag, pk=tag.id)
            recipe.tags.add(current_tag)

        for ingredient in ingredients:
            IngredientRecipe.objects.get_or_create(
                ingredient=ingredient['id'], recipe=recipe,
                amount=ingredient['amount'],
            )
        return recipe

    def update(self, instance, validated_data):
        """
        Adds new ingredients to recipe and deletes those that are not in the
        request
        """
        ingredients = validated_data.pop('ingredients')
        ingredient_objs = []
        for ingredient in ingredients:
            ingredient_objs.append(ingredient['id'])
            IngredientRecipe.objects.get_or_create(
                ingredient=ingredient['id'], recipe=instance,
                amount=ingredient['amount'],
            )
        ingredients = IngredientRecipe.objects.filter(recipe=instance)
        for ingredient in ingredients:
            if ingredient.ingredient not in ingredient_objs:
                IngredientRecipe.objects.get(
                    recipe=instance, ingredient=ingredient.ingredient,
                ).delete()
        return super().update(instance, validated_data)


class RecipeListRetrieveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientRecipeSerializer(
        many=True, source='ingredient_recipe'
    )
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
            return obj.favorite.all().exists()

        return None

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.shopping_cart.all().exists()

        return None


class CreateDeleteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    recipe = serializers.SerializerMethodField()

    class Meta:
        model = None
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        instance = get_object_or_404(
            Recipe, pk=int(self._context['view'].kwargs['recipe_id'])
        )
        return RecipeSerializer(instance, context=context).data

    def get_user(self, obj):
        return self.context['request'].user

    def get_recipe(self, obj):
        return get_object_or_404(
            Recipe, pk=self._context['view'].kwargs['recipe_id']
        )

    def validate(self, attrs):
        obj = self.Meta.model.objects.filter(
            user=self.context['request'].user,
            recipe=self.context['view'].kwargs['recipe_id']
        ).first()
        if obj is not None:
            raise serializers.ValidationError(
                'Such record is already exists'
            )
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context['request'].user
        obj = get_object_or_404(
            Recipe, pk=self.context['view'].kwargs['recipe_id'],
        )
        return self.Meta.model.objects.create(user=user, recipe=obj)
