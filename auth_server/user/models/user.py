from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        """
        일반 사용자 계정 생성
        """
        if (not username) and (not password):
            raise ValueError("유저명과 비밀번호는 반드시 있어야 합니다.")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        슈퍼(관리자) 계정 생성
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("스태프 설정이 일치하지 않습니다.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼 유저로 설정되지 않았습니다.")

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="유저 식별 아이디",
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    objects = UserManager()  # 커스텀 매니저로 유저 생성

    USERNAME_FIELD = "username"  # 로그인 시 사용할 필드

    def __str(self):
        return self.username
