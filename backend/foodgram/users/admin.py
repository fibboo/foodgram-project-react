from django.contrib import admin

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed',)
    list_select_related = ('subscriber', 'subscribed',)


admin.site.register(Subscription, SubscriptionAdmin)
