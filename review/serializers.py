from rest_framework import serializers
from .models import Review, Like, Comment

class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_nickname', 'book', 'content', 'rating', 'created_at', 'updated_at', 'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'review']

class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_nickname', 'review', 'content', 'created_at', 'updated_at']
