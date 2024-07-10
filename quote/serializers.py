from rest_framework import serializers

from language.serializers import LanguageSerializer
from .models import Quote, QuoteTranslation


class QuoteTranslationSerializer(serializers.ModelSerializer):
    lang = LanguageSerializer(read_only=True)

    class Meta:
        model = QuoteTranslation
        fields = '__all__'


class QuoteSerializer(serializers.ModelSerializer):
    translations = QuoteTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Quote
        fields = '__all__'
