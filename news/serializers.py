from rest_framework import serializers

from language.serializers import LanguageSerializer
from user.serializers import UserSerializer
from .models import News, NewsTranslation, NewsTag, Comment, VoteComment, Link
from tags.serializers import TagSerializer
from quote.serializers import QuoteSerializer
from tags.models import Tag
from language.models import Language
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
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'user_id', 'news', 'created_at']


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
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return f"https://{request.get_host().split(':')[0]}:8443{obj.image.url}"
        return None

    class Meta:
        model = News
        fields = '__all__'

# class NewsCreateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = News
#         fields = ['author', 'id','image', 'category','subcategory','exclusive','is_published' ]

class NewsTranslationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTranslation
        fields = ['lang', 'title', 'text']

class NewsTagCreateSerializer(serializers.ModelSerializer):
    tag = serializers.IntegerField()

    class Meta:
        model = NewsTag
        fields = ['tag']


class LinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            'facebook', 'whatsapp', 'telegram', 'vk',
            'twitter', 'threads', 'instagram', 'linkedin',
            'youtube', 'tiktok'
        ]


class NewsCreateSerializer(serializers.ModelSerializer):
    translations = NewsTranslationCreateSerializer(many=True, required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    links = LinkCreateSerializer(many=True, required=False)

    class Meta:
        model = News
        fields = [
            'id', 'author', 'image', 'category', 'subcategory',
            'exclusive', 'is_published', 'quote',
            'translations', 'tags', 'links'
        ]

    def create(self, validated_data):
        translations_data = validated_data.pop('translations', [])
        tags_data = validated_data.pop('tags', [])
        links_data = validated_data.pop('links', [])

        # Создание экземпляра News
        news_instance = News.objects.create(**validated_data)

        # Создание NewsTranslations
        for translation_data in translations_data:
            NewsTranslation.objects.create(news=news_instance, **translation_data)

        # Установление ManyToMany связей для тегов
        news_instance.tags.set(tags_data)

        # Создание Links
        for link_data in links_data:
            Link.objects.create(new_id=news_instance, **link_data)

        return news_instance

class NewsShortSerializer(serializers.ModelSerializer):
    translations = NewsTranslationSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return f"http://{request.get_host().split(':')[0]}:1337{obj.image.url}"
        return None

    class Meta:
        model = News
        fields = ['id', 'author', 'translations', 'category', 'image', 'created_at', 'updated_at']


class VoteCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = VoteComment
        fields = '__all__'
