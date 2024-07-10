from rest_framework import serializers

from language.serializers import LanguageSerializer
from .models import Tag, TagTranslation


class TagTranslationSerializer(serializers.ModelSerializer):
    lang = LanguageSerializer(read_only=True)

    class Meta:
        model = TagTranslation
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    translations = TagTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'
