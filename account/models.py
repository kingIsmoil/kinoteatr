from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import random

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.generate_verification_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def generate_verification_code(self):
        """Генерирует 6-значный код подтверждения"""
        self.verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return self.verification_code