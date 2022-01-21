from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipes',)
router.register('tags', views.TagMixinView, basename='tags', )
router.register(
    'ingredients', views.IngredientMixinView, basename='ingredients'
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    views.CreateDeleteView, basename='favorite',
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    views.CreateDeleteView, basename='shopping_cart',
)

urlpatterns = [
    path('recipes/download_shopping_cart/',
         views.DownloadShoppingCartView.as_view(),
         name='download_shopping_cart'),
    path('recipes/send_shopping_cart_to_telegram/',
         views.DownloadShoppingCartView.as_view(),
         name='send_shopping_cart_to_telegram'),
    path('', include(router.urls)),
]
