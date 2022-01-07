from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register(
    'subscriptions', views.SubscriptionView, basename='subscriptions',
)

urlpatterns = [
    url('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path('users/', include(router.urls)),
]
