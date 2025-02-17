from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
            
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=80, unique=True)
    favorite_cities = models.JSONField(default=list)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def add_favorite_city(self, city):
        if not self.favorite_cities:
            self.favorite_cities = []
        if city not in self.favorite_cities:
            self.favorite_cities.append(city)
            self.save()

    def remove_favorite_city(self, city):
        if self.favorite_cities and city in self.favorite_cities:
            self.favorite_cities.remove(city)
            self.save()

    def save(self, *args, **kwargs):
        # Ensure email is normalized before saving
        if self.email:
            self.email = self.email.lower().strip()
        if not self.favorite_cities:
            self.favorite_cities = []
        super().save(*args, **kwargs)
