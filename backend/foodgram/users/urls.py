from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
