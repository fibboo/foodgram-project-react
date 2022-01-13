from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Name', max_length=200, unique=True,)
    color = models.CharField('Color', max_length=7, unique=True,)
    slug = models.SlugField(unique=True,)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Name', max_length=200)
    measurement_unit = models.CharField('Measurement unit', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ingredients', through='IngredientRecipe',
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Tags', through='TagRecipe',
    )
    image = models.ImageField('Image')
    author = models.ForeignKey(
        User, verbose_name='Author', on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField('Name', max_length=200)
    text = models.TextField('Description')
    cooking_time = models.IntegerField(
        'Cooking time', validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def get_ingredients(self):
        return "\n".join([i.name for i in self.ingredients.all()])

    def get_tags(self):
        return "\n".join([i.name for i in self.tags.all()])

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тег - Рецепт'
        verbose_name_plural = 'Теги - Рецепты'

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient_recipe',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredient_recipe',
    )
    amount = models.IntegerField(
        'Amount', validators=[MinValueValidator(0.1)],
    )

    class Meta:
        verbose_name = 'Ингредиент - Рецепт'
        verbose_name_plural = 'Ингредиенты - Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique ingredient for recipe',
            ),
        ]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'
