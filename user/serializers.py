from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email']

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if User.objects.filter(nickname=data.get('nickname')).exists():
            raise serializers.ValidationError({"nickname": "이미 사용 중인 닉네임입니다."})
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({"email": "이미 등록된 이메일입니다."})
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
