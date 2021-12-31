import django_filters

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags__slug')
    is_favorited = django_filters.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart',)

    # to-do don't like implementation. Rewrite
    def filter_is_favorited(self, queryset, name, value):
        if value == 1:
            if self.request.user.is_authenticated:
                return queryset.filter(favorite_recipe__user=self.request.user)
            return queryset
        return queryset.filter(favorite_recipe__user__isnull=True)

    # to-do don't like implementation. Rewrite
    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value == 1:
            if self.request.user.is_authenticated:
                return queryset.filter(
                    shopping_cart_recipe__shopping_cart__user__pk=self.request.user.id
                )
            return queryset.none()
        return queryset.filter()
