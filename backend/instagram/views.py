from datetime import timedelta
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    # 쿼리 갯수를 줄이는게 정답은 아니지만 포스팅 목록이 많아질 수록 쿼리가 많아지기 때문에 최적화가 필요
    queryset = Post.objects.all().select_related("author").prefetch_related("tag_set", "like_user_set")
    serializer_class = PostSerializer
    # permission_classes = [AllowAny,] # FIXME: 인증적용

    def get_queryset(self):
        timesince = timezone.now() - timedelta(days=3) 
        qs =  super().get_queryset()
        qs = qs.filter(
            Q(author=self.request.user) | # 자신이 작성한 글이나
            Q(author__in=self.request.user.following_set.all()) # 팔로잉 하고 있는 유저의 글
        )
        qs = qs.filter(created_at__gte=timesince) # 최근 3일 글 목록
        # qs을 이어서 쓰면 체이닝되어 &조건으로 다 들어감
        return qs