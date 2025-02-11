from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser,PermissionsMixin):
    phone_number = models.CharField(max_length=11,unique=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('email','full_name')

    objects = UserManager()

    def __str__(self):
        return self.email


    @property
    def is_staff(self):
        return self.is_admin

class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code}'
