from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, is_author, password=None):
        """
        Creates and saves a User with the given username, is_author flag, and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username = username,
            is_author = is_author,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, is_author, password=None):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username,
            password = password,
            is_author = is_author,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name = 'username',
        max_length = 60,
        unique = True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name="first name", max_length=50)
    last_name = models.CharField(verbose_name="last name", max_length=50)
    is_author = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['is_author','first_name','last_name']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin