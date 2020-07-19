from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'name', 'avatar_url']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True) # 여러개라면 many=True 지정
    class Meta:
        model = Post
        fields = '__all__'
        