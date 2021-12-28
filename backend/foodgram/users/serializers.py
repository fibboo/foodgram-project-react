from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, validators

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

    # to-do. handle possible error
    def create(self, validated_data):
        user = super().create(validated_data)
        ShoppingCart.objects.create(user=user)

        return user


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    # don't like implementation. Rewrite
    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            subscription = Subscription.objects.filter(
                subscriber=self.context['request'].user,
                subscribed=obj
            ).first()
        else:
            subscription = None
        return subscription is not None
