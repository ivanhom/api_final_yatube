from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from api.permissions import IsOwnerOrReadOnly, ReadOnly
from api.serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)
from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для объектов модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Представление для объектов модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'group')

    def get_permissions(self):
        """Изменение разрешений, если получен GET запрос."""
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return (IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly())

    def perform_create(self, serializer):
        """Сохранение автора при создинии публикации."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для объектов модели Comment."""
    serializer_class = CommentSerializer

    def get_permissions(self):
        """Изменение разрешений, если получен GET запрос."""
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return (IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly())

    def get_queryset(self):
        """Получение набора комментариев для запрашиваемой публикации."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        """Сохранение комментария для запрашиваемой публикации."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Представление для объектов модели Follow."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Получение набора подписок для запрашиваемого пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Сохранение подписки для запрашиваемого пользователя."""
        serializer.save(user=self.request.user)
