from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework import viewsets
from .models import  Tag, TagTranslation
from .serializers import TagSerializer, TagTranslationSerializer


class TagViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagTranslationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = TagTranslation.objects.all()
    serializer_class = TagTranslationSerializer
