from djoser.serializers import TokenSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        ref_name = 'MyAppUserSerializer'
