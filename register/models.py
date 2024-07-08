import uuid
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
    
    def create_superuser(self, email, firstName, lastName, password=None):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, firstName, lastName, password)


class User(AbstractBaseUser):
    userId = models.CharField(default=generate_uuid, unique=True, max_length=36, editable=False)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email

class Organisation(models.Model):
    org_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='organisations')

    def __str__(self):
        return self.name