from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api import messages
from posts.models import Comment, Follow, Group, Post, User


class GroupSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Group."""
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Post."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    pub_date = serializers.DateTimeField(read_only=True)
    image = serializers.ImageField(default=None)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    created = serializers.DateTimeField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
        required=False
    )

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=messages.UNIQUE_FOLLOWING_VALIDATION_ERROR
            ),
        )

    def validate(self, value):
        """Проверка при попытке пользователя подписаться на самого себя."""
        if self.context.get('request').user == value.get('following'):
            raise serializers.ValidationError(
                messages.SELF_FOLLOWING_VALIDATION_ERROR
            )
        return value
