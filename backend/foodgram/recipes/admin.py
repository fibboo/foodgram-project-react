from django.contrib import admin

from . import models


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color',)
    search_fields = ('name', 'color',)
    list_filter = ('color',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('measurement_unit',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'cooking_time', 'get_ingredients', 'get_tags',
    )
    filter_horizontal = ('ingredients', 'tags',)
    list_select_related = ('author',)
    search_fields = ('name', 'author',)
    list_filter = ('cooking_time', 'author',)


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'recipe',)
    list_select_related = ('tag', 'recipe',)
    search_fields = ('recipe',)
    list_filter = ('tag',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe',)
    list_select_related = ('ingredient', 'recipe',)
    search_fields = ('recipe', 'ingredient',)


admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.TagRecipe, TagRecipeAdmin)
admin.site.register(models.IngredientRecipe, IngredientRecipeAdmin)
