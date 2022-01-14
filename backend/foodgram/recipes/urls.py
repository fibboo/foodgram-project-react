from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipes',)
router.register('tags', views.TagMixinView, basename='tags', )
router.register(
    'ingredients', views.IngredientMixinView, basename='ingredients'
)


urlpatterns = [
    path('', include(router.urls))
]
