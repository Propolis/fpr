from django.urls import include, path
from rest_framework import routers


from .views import TagViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
urlpatterns = router.urls
