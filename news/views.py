from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import viewsets
from .models import News, Comment
from .serializers import NewsSerializer, CommentSerializer, NewsShortSerializer


class NewsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  # Увеличиваем количество просмотров
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class NewsShortViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsShortSerializer

class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



