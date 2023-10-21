from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: str) -> object:
        if not password:
            raise ValueError('Email is Required')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str = None) -> object:
        if not username:
            raise ValueError('Username id Required')
        if not password:
            return ValueError('Password id Required')
        user = self.create_user(username=username, email=self.normalize_email(email), password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self) -> str:
        return f'{self.username}, {self.email}'
