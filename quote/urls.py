from rest_framework.routers import DefaultRouter
from .views import QuoteViewSet, QuoteTranslationViewSet

router = DefaultRouter()

router.register('quote', QuoteViewSet)
router.register(r'quote_translation', QuoteTranslationViewSet)
