from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

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
