from django.contrib import admin

from .models import Subscribe


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed',)
    list_select_related = ('subscriber', 'subscribed',)


admin.site.register(Subscribe, SubscribeAdmin)
