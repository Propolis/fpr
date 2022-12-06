from django.urls import include, path
from rest_framework import routers


from .views import (
    TagViewSet,
    RecipeViewSet,
)

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
