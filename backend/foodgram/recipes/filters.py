from django_filters.rest_framework import filters, FilterSet
from rest_framework.filters import SearchFilter

from .models import Recipe


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart',)


    def filter_is_favorited(self, queryset, name, value):
        if value == 1:
            if self.request.user.is_authenticated:
                return queryset.filter(favorite_recipe__user=self.request.user)
            return queryset
        return queryset.filter(favorite_recipe__user__isnull=True)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value == 1:
            if self.request.user.is_authenticated:
                return queryset.filter(
                    shopping_cart_recipe__shopping_cart__user__pk=
                    self.request.user.id
                )
            return queryset.none()
        return queryset.filter()


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
