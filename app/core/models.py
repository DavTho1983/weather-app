from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
            Creates and saves a new user,
            with password allowed to be empty so we can
            create a user on their behalf and let them change the password
        """

        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)  # because domain name not case sensitive
        user.set_password(password)  # password needs to be set via function because encrypted
        user.save(using=self._db)  # required for supporting multiple databases

        return user

    def create_staff_user(self, email, password):
        """Creates and saves a new staff user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
