from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .utils import generate_uuid

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not firstName:
            raise ValueError('The First Name field must be set')
        if not lastName:
            raise ValueError('The last Name field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, firstName=firstName, lastname=lastName)
        user.set_password(password)
        user.save(using=self.db)
        return user