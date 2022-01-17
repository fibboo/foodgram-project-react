from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, permissions
from rest_framework.permissions import AllowAny

from .filters import RecipeFilter, IngredientSearchFilter
from .models import Recipe, Tag, Ingredient, Favorite
from . import serializers
from .pagination import EmptyPagination
from .permissions import IsAuthorAdminOrReadOnly


class RetrieveListMixinView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.RecipeListRetrieveSerializer
        else:
            return serializers.RecipeCreateUpdateDestroySerializer


class TagMixinView(RetrieveListMixinView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = EmptyPagination


class IngredientMixinView(RetrieveListMixinView):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = EmptyPagination
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class FavoriteCreateDeleteView(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    queryset = Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = EmptyPagination

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_id'])
        favorite = get_object_or_404(
            Favorite, user=user, recipe=recipe,
        )
        obj = queryset.get(pk=favorite.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
