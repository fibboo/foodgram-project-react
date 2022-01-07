from django.contrib.auth import get_user_model
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


class SubscriptionSerializer(serializers.ModelSerializer):
    # subscribed = CustomUserSerializer(read_only=True)
    # recipes = RecipeSerializer(many=True)

    class Meta:
        model = Subscription
        # fields = ('subscribed', 'recipes', 'recipes_count',)
        fields = '__all__'

    # def get_recipes_count(self, obj):
    #     return obj.subscribed.author
