from django.contrib import admin

from . import models


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed',)
    list_select_related = ('subscriber', 'subscribed',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_select_related = ('user', 'recipe',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_recipes',)
    list_select_related = ('user',)


class ShoppingCartRecipeAdmin(admin.ModelAdmin):
    list_display = ('shopping_cart', 'recipe',)
    list_select_related = ('shopping_cart', 'recipe',)


admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.Favorite, FavoriteAdmin)
admin.site.register(models.ShoppingCartRecipe, ShoppingCartRecipeAdmin)
admin.site.register(models.ShoppingCart, ShoppingCartAdmin)
