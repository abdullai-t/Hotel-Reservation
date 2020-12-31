from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings


class UserManager(auth_models.BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have email")

        if not username:
            raise ValueError("Users must have Username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_manager = True

        user.save(using=self._db)
        return user


class User(auth_models.AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=150, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    fname = models.CharField(max_length=50,blank=True, null=True)
    lname = models.CharField(max_length=50,blank=True, null=True)
    isBlackListed = models.BooleanField(blank=True, null=True, default=False)
    nationality = models.CharField(max_length=50,blank=True, null=True)
    homeAddress = models.CharField(max_length=50,blank=True, null=True)
    phone = models.CharField(max_length=50,blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(sef, app_label):
        return True

    objects = UserManager()


class Staff(models.Model):
    fname = models.CharField(max_length=50,blank=True, null=True)
    lname = models.CharField(max_length=50,blank=True, null=True)
    job = models.CharField(max_length=50,blank=True, null=True)
    idNumber = models.CharField(max_length=50,blank=True, null=True)
    nationality = models.CharField(max_length=50,blank=True, null=True)
    email = models.EmailField(max_length=50,blank=True, null=True)
    homeAddress = models.CharField(max_length=50,blank=True, null=True)
    phone = models.CharField(max_length=50,blank=True, null=True)

    def __str__(self):
        return self.fname