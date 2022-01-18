from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F

from recipes.models import Recipe

User = get_user_model()


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriber')
    subscribed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribed')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscribed'],
                name='unique_following',
            ),
            models.CheckConstraint(
                check=~Q(subscribed=F('subscriber')),
                name='not_following_yourself',
            ),
        ]

    def __str__(self):
        return f'{self.subscriber} {self.subscribed}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, verbose_name='User', on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe, verbose_name='Recipe', on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='already in shopping cart',
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
