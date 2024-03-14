from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    profile_name = models.CharField(max_length=150, unique=False)
    #first_name = None
    #last_name = None
    bio = models.TextField(max_length=150)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["profile_name"]

    def __str__(self):
        return self.username


