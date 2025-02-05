from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email']

class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'nickname', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_nickname(self, value):
        """ 닉네임 중복 검사 """
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def validate_email(self, value):
        """ 이메일 중복 검사 """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 등록된 이메일입니다.")
        return value

    def validate(self, data):
        """ 비밀번호 확인 검증 """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        """ 비밀번호 해싱 후 저장 """
        validated_data.pop('password2')  # password2는 저장할 필요 없음
        validated_data['password'] = make_password(validated_data['password'])  # 비밀번호 해싱
        return User.objects.create(**validated_data)
