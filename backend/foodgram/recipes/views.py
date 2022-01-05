from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, permissions
from rest_framework.permissions import AllowAny

from recipes.filters import RecipeFilter
from recipes.models import Recipe, Tag, Ingredient
from recipes import serializers
from recipes.pagination import EmptyPagination
from recipes.permissions import IsAuthorAdminOrReadOnly


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
