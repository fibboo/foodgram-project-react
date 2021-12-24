from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Author', on_delete=models.CASCADE,
        related_name='author',
    )


class Tag(models.Model):
    name = models.CharField('Name', max_length=15, unique=True,)
    color = models.CharField('Color', max_length=7, unique=True,)
    slug = models.SlugField(unique=True,)
    recipe = models.ForeignKey(
        Recipe, verbose_name='Recipe', on_delete=models.SET_NULL,
        related_name='tag', blank=True, null=True,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Name', unique=True,)
    measurement_unit = models.CharField('Measurement unit')
    recipe = models.ForeignKey(
        Recipe, verbose_name='Recipe', on_delete=models.SET_NULL,
        related_name='recipe', blank=True, null=True,
    )
    amount = models.IntegerField('Amount', blank=True, null=True)
