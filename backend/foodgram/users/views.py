from rest_framework import viewsets, mixins

from users.models import Subscription
from users.serializers import SubscriptionSerializer


class SubscriptionView(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
