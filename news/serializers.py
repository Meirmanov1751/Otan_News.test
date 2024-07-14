from rest_framework import serializers

from language.serializers import LanguageSerializer
from user.serializers import UserSerializer
from .models import News, NewsTranslation, NewsTag, Comment, VoteComment, Link
from tags.serializers import TagSerializer
from quote.serializers import QuoteSerializer


class NewsTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)

    class Meta:
        model = NewsTag
        fields = ('tag',)


class NewsTranslationSerializer(serializers.ModelSerializer):
    lang = LanguageSerializer(read_only=True)

    class Meta:
        model = NewsTranslation
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    translations = NewsTranslationSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    quote = QuoteSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = '__all__'


class NewsShortSerializer(serializers.ModelSerializer):
    translations = NewsTranslationSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'author', 'translations', 'category', 'image', 'created_at', 'updated_at']


class VoteCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = VoteComment
        fields = '__all__'
