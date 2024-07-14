from rest_framework.routers import DefaultRouter
from .views import TagViewSet, TagTranslationViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'tags_translation', TagTranslationViewSet)
