from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, F


class User(AbstractUser):
    """
    Redefined User model with telegram_id field
    """
    telegram_id = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']


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
