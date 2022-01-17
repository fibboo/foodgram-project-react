from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, pagination

from recipes.pagination import EmptyPagination
from .models import Subscription
from .serializers import (
    SubscriptionListSerializer, SubscriptionCreateDestroySerializer, )

User = get_user_model()


class SubscriptionListView(mixins.ListModelMixin, viewsets.GenericViewSet, ):
    serializer_class = SubscriptionListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return User.objects.filter(subscribed__subscriber=self.request.user)


class SubscriptionCreateDestroyView(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionCreateDestroySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = EmptyPagination

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        subscriber = self.request.user
        subscribed = get_object_or_404(User, pk=self.kwargs['user_id'])
        subscription = get_object_or_404(
            Subscription, subscriber=subscriber, subscribed=subscribed,
        )
        obj = queryset.get(pk=subscription.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
