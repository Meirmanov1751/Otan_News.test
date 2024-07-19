import logging
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import viewsets
from .models import News, Comment
from .serializers import NewsSerializer, CommentSerializer, NewsShortSerializer, CommentCreateSerializer
from .filters import NewsFilter, CommentFilter, SubscriberFilter

logger = logging.getLogger('comments')


class NewsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        limit = self.request.query_params.get('limit')
        order_by = self.request.query_params.get('order_by')

        if order_by:
            queryset = queryset.order_by(order_by)

        if limit:
            queryset = queryset[:int(limit)]

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  # Увеличиваем количество просмотров
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class NewsShortViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsShortSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        limit = self.request.query_params.get('limit')
        order_by = self.request.query_params.get('order_by')

        if order_by:
            queryset = queryset.order_by(order_by)

        if limit:
            queryset = queryset[:int(limit)]

        return queryset


class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        comment = serializer.save()
        logger.info(f'New comment {comment.comment}')
