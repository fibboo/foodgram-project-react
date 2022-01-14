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


class Favorite(models.Model):
    user = models.ForeignKey(
        User, verbose_name='User', on_delete=models.CASCADE,
        related_name='favorite_user'
    )
    recipe = models.ForeignKey(
        Recipe, verbose_name='Recipe', on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User, verbose_name='User', on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipes = models.ManyToManyField(
        Recipe, verbose_name='Ingredients', through='ShoppingCartRecipe',
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='only one shopping cart for user',
            ),
        ]

    def get_recipes(self):
        return "\n".join([i.name for i in self.recipes.all()])

    def __str__(self):
        return f'{self.user}\' shopping cart'


class ShoppingCartRecipe(models.Model):
    shopping_cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE,
        # related_name='shopping_cart_recipe',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart_recipe',
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'

    def __str__(self):
        return f'{self.recipe} in {self.shopping_cart}'
