from django.urls import include, path
from rest_framework import routers

from .views import (
    IngredientViewSet,
    TagViewSet,
    RecipeViewSet,
    SubscribeView,
    ListOnlySubscriptionAPIView
)

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/<int:pk>/subscribe/',
        SubscribeView.as_view(),
        name='users-detail-subscribe'
    ),
    path(
        'users/subscriptions/',
        ListOnlySubscriptionAPIView.as_view(),
        name='users-subscribtions'
    ),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
