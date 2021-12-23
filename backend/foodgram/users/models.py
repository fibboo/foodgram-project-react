from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriber')
    subscribed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribed')
