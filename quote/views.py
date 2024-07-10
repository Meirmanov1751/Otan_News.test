from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework import viewsets
from .models import Quote, QuoteTranslation
from .serializers import QuoteSerializer, QuoteTranslationSerializer

class QuoteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

class QuoteTranslationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = QuoteTranslation.objects.all()
    serializer_class = QuoteTranslationSerializer
