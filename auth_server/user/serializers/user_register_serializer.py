from user.models.user import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # 클라이언트 측으로 반환되지 않게 방지
        required=True,
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password_confirm",
        ]

    def validate(self, data):
        """비밀번호 확인 검증"""
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        if password != password_confirm:
            raise ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")

        return data

    def create(self, validated_data):
        """유저 모델 생성"""
        username = validated_data["username"]
        password = validated_data["password"]
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        return user
