from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, permissions

from recipes.pagination import EmptyPagination
from users.models import Subscription
from users.serializers import (
    SubscriptionListSerializer, SubscriptionCreateDestroySerializer, )

User = get_user_model()


class SubscriptionListView(mixins.ListModelMixin, viewsets.GenericViewSet, ):
    serializer_class = SubscriptionListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(subscribed__subscriber=self.request.user)


class SubscriptionCreateDestroyView(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionCreateDestroySerializer
    pagination_class = EmptyPagination
