from rest_framework import mixins, permissions, viewsets

from recipes.pagination import EmptyPagination


class RetrieveListMixinView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (permissions.AllowAny,)


class CreateDestroyMixinView(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = EmptyPagination
