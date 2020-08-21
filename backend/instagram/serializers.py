from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'name', 'avatar_url']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True) # 여러개라면 many=True 지정
    is_like = serializers.SerializerMethodField('is_like_field')

    def is_like_field(self, post):
        # 사용자를 받아와야하는데 self.request.user 은 view 즉 cbv에서 사용가능한데 여기서는 사용이 안된다 => (drf context사용)
        if 'request' in self.context:
            user = self.context['request'].user
            return post.like_user_set.filter(pk=user.pk).exists()
        return False

    class Meta:
        model = Post
        fields = ['id', 'author', 'created_at', 'photo', 'caption', 'location', 'tag_set', 'is_like']
    

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "message", "created_at"]