from django.contrib import admin

from . import models


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed',)
    list_select_related = ('subscriber', 'subscribed',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_select_related = ('user', 'recipe',)


admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.ShoppingCart, ShoppingCartAdmin)
