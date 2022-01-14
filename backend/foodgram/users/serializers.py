from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, validators

from recipes.models import Recipe
from users.models import Subscription, ShoppingCart

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password',
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'You should not use "me" as a username'
            )
        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        ShoppingCart.objects.get_or_create(user=user)

        return user


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            return Subscription.objects.filter(
                subscriber=self.context['request'].user, subscribed=obj
            ).exists()

        return None


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionListSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )

    def get_recipes(self, obj):
        recipes_limit = (
            self.context['request'].query_params.get('recipes_limit')
        )
        try:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        except ValueError:
            recipes = obj.recipes.all()
        return RecipeSerializer(recipes, many=True, read_only=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionCreateDestroySerializer(serializers.ModelSerializer):
    subscriber = serializers.SerializerMethodField()
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        instance = get_object_or_404(
            User, pk=int(self._context['view'].kwargs['user_id'])
        )
        return SubscriptionListSerializer(instance, context=context).data

    def get_subscriber(self, obj):
        return self.context['request'].user

    def get_subscribed(self, obj):
        return get_object_or_404(
            User, pk=self._context['view'].kwargs['user_id'],
        )

    def validate(self, attrs):
        request_user_id = self.context['request'].user.id
        to_subscribe_user_id = int(self._context['view'].kwargs['user_id'])
        if request_user_id == to_subscribe_user_id:
            raise serializers.ValidationError(
                'You can not subscribe to yourself'
            )
        subscription = Subscription.objects.filter(
            subscriber=self.context['request'].user,
            subscribed=self._context['view'].kwargs['user_id']
        ).first()
        if subscription is not None:
            raise serializers.ValidationError(
                'Already following'
            )
        return super().validate(attrs)

    def create(self, validated_data):
        subscriber = self.context['request'].user
        subscribed = get_object_or_404(
            User, pk=self._context['view'].kwargs['user_id'],
        )
        subscription = Subscription.objects.create(
            subscriber=subscriber,
            subscribed=subscribed,
        )
        return subscription
