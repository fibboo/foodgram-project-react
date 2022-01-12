from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register(
    r'users/(?P<user_id>\d+)/subscriptions',
    views.SubscriptionView, basename='subscriptions',
)

urlpatterns = [
    url('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
