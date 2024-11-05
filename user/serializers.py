from djoser.serializers import TokenSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from news.models import News
from django.db.models import Sum

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'first_name', 'last_name', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class ConfirmCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    news_count = serializers.SerializerMethodField()
    total_news_views = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'role', 'first_name', 'last_name', 'phone_number',
            'news_count', 'total_news_views'
        ]
        ref_name = 'MyAppUserSerializer'

    def get_news_count(self, user):
        # Count the number of news posts for this user
        return News.objects.filter(author=user).count()

    def get_total_news_views(self, user):
        # Sum the views of all news posts for this user
        return News.objects.filter(author=user).aggregate(total_views=Sum('views'))['total_views'] or 0