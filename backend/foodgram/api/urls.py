from django.urls import include, path
from rest_framework import routers

from .views import TagViewSet

router = routers.SimpleRouter()
router.register('tags', TagViewSet)
urlpatterns = router.urls
urlpatterns += [
    path('auth/', include('djoser.urls')),
]
