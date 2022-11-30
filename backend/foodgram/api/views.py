from django.shortcuts import get_object_or_404, render
from recipes.models import Tag
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
