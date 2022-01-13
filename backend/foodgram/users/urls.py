from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register(
    r'users/subscriptions', views.SubscriptionListView,
    basename='subscriptions',
)
router.register(
    r'users/(?P<user_id>\d+)/subscriptions',
    views.SubscriptionCreateDestroyView, basename='subscriptions',
)

urlpatterns = [
    path('', include(router.urls)),
    url('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
