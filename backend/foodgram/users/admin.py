from django.contrib import admin

from . import models


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed',)
    list_select_related = ('subscriber', 'subscribed',)


class TagAdmin(admin.ModelAdmin):
    list = ('name', 'color' 'slug',)
    readonly_fields = ('slug',)


admin.site.register(models.Subscription, SubscriptionAdmin)
