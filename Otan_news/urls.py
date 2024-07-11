from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from language.urls import router as post_language
from news.sitemaps import NewsSitemap
from news.urls import router as post_news
from quote.sitemaps import QuoteSitemap
from tags.urls import router as post_tags
from quote.urls import router as post_quote

router = DefaultRouter()
router.registry.extend(post_language.registry)
router.registry.extend(post_news.registry)
router.registry.extend(post_tags.registry)
router.registry.extend(post_quote.registry)

sitemaps = {
    'news': NewsSitemap,
    'quotes': QuoteSitemap,
}

urlpatterns = [
    path('', schema_view),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
