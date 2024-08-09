import logging
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import viewsets
from .models import News, Comment
from .serializers import NewsSerializer, NewsCreateSerializer, CommentSerializer, NewsShortSerializer, CommentCreateSerializer
from .filters import NewsFilter, CommentFilter, SubscriberFilter

logger = logging.getLogger('comments')

class NewsPagination(LimitOffsetPagination):
    default_limit = None
    max_limit = 100

    def paginate_queryset(self, queryset, request, view=None):
        limit = request.query_params.get('limit')
        if limit is None:
            return None
        return super().paginate_queryset(queryset, request, view)

class NewsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
    pagination_class = NewsPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.query_params.get('order_by')

        if order_by:
            queryset = queryset.order_by(order_by)


        return queryset

class NewsCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    




class NewsShortViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsShortSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
    pagination_class = NewsPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.query_params.get('order_by')

        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


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
