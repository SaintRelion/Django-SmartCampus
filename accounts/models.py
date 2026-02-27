from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    employeeId = models.CharField(max_length=20, null=True)
