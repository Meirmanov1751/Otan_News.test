from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, CommentViewSet, NewsShortViewSet

router = DefaultRouter()

router.register('news', NewsViewSet, basename='news')
router.register('news_short', NewsShortViewSet, basename='news_short')
router.register(r'comments', CommentViewSet)
