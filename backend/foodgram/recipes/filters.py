import django_filters

from .models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags__slug')
    # is_favorited = django_filters.NumberFilter()

    class Meta:
        model = Recipe
        fields = (
            'author', 'tags',
            # 'is_favorited', 'is_in_shopping_cart',
        )
