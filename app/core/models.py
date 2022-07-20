"""
Database models.
"""
from unicodedata import name
from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for the user"""

    def create_user(self, email, password=None, **extrafields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extrafields)
        user.set_password(password)
        user.save(using= self._db)

        return user

    def create_superuser(self, email, password, **fields):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

# create User Table/ Benutzer
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

###############################
# # create Module Table/ Modul Tabelle
# class Module(models.Modul):
#     name = models.CharField(max_length=255)
#     prof = models.CharField(max_length=255)
#     semester = models.CharField(max_length=255)
#     is_active = models.Booleanfield(default=True)

# # create Homework Table /Abgaben Tabelle
# class Homework(models.Modul):
#     text = models.TextField()
