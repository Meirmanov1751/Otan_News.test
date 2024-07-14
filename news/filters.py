# filters.py
import django_filters
from django_filters import rest_framework as filters
from .models import News, Comment, Subscriber


class NewsFilter(filters.FilterSet):
    category = filters.CharFilter(lookup_expr='icontains')
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='icontains')
    comments = django_filters.CharFilter(field_name='comments__content', lookup_expr='icontains')

    class Meta:
        model = News
        fields = ['category', 'tags', 'comments']


class CommentFilter(filters.FilterSet):
    content = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Comment
        fields = '__all__'


class SubscriberFilter(filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Subscriber
        fields = '__all__'
