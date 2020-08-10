from datetime import timedelta
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    # 쿼리 갯수를 줄이는게 정답은 아니지만 포스팅 목록이 많아질 수록 쿼리가 많아지기 때문에 최적화가 필요
    queryset = Post.objects.all().select_related("author").prefetch_related("tag_set", "like_user_set")
    serializer_class = PostSerializer
    # permission_classes = [AllowAny,] # FIXME: 인증적용

    # drf 에서 임의의 값을 context로 넘겨줄 수 있는데 현재유저를 가져오기 위해 사용
    def get_serializer_context(self):   
        context =  super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        # timesince = timezone.now() - timedelta(days=3) 
        qs =  super().get_queryset()
        qs = qs.filter(
            Q(author=self.request.user) | # 자신이 작성한 글이나
            Q(author__in=self.request.user.following_set.all()) # 팔로잉 하고 있는 유저의 글
        )
        # qs = qs.filter(created_at__gte=timesince) # 최근 3일 글 목록
        # qs을 이어서 쓰면 체이닝되어 &조건으로 다 들어감
        return qs
    
    def perform_create(self, serializer):
        # form에서는 이렇게 가능하지만.. drf에서 인자로 넘겨준다
        # post = form.save(commit=False)
        # post.author = self.request.user
        # post.save()
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)

    @action(detail=True, methods=["POST"])
    def like(self, request, pk):
        post = self.get_object() # ModelViewSet에서 구현이 되어 있기때문에 굳이 get_object_404 할 필요 X
        post.like_user_set.add(self.request.user)
        return Response(status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self, request, pk):
        post = self.get_object()
        post.like_user_set.remove(self.request.user)
        return Response(status.HTTP_204_NO_CONTENT)