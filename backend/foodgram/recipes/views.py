from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from users.models import ShoppingCart
from .filters import RecipeFilter, IngredientSearchFilter
from .models import Recipe, Tag, Ingredient, Favorite, IngredientRecipe
from . import serializers
from .pagination import EmptyPagination
from .permissions import IsAuthorAdminOrReadOnly


class RetrieveListMixinView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (AllowAny,)


class CreateDestroyMixinView(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = EmptyPagination


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


class CreateDeleteView(CreateDestroyMixinView):

    def get_model(self):
        if self.basename == 'favorite':
            return Favorite
        return ShoppingCart

    def get_serializer_class(self):
        serializers.CreateDeleteSerializer.Meta.model = self.get_model()
        return serializers.CreateDeleteSerializer

    def get_object(self):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_id'])
        obj = get_object_or_404(
            self.get_model(), user=user, recipe=recipe,
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DownloadShoppingCartViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=self.request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
            'ingredient__name').annotate(ingredient_total=Sum('amount'))

    def generate_file(self):
        lines = []
        for ingredient in self.get_queryset():
            lines.append(f'{ingredient["ingredient__name"]}:'
                         f'{ingredient["ingredient_total"]} '
                         f'{ingredient["ingredient__measurement_unit"]} \n')
        return lines

    def get(self, request):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename=список-покупок.txt')
        response.writelines(self.generate_file())
        return response
