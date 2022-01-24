from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed',)
    list_select_related = ('subscriber', 'subscribed',)


admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.User, UserAdmin)
