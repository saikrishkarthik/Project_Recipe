# Create your models here.
from django.db import models


class LoginUser(models.Model):
    username = models.CharField(max_length=100, unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    token = models.TextField(null=True)
    is_active = models.BooleanField(default=True, null=True)
    
    def __str__(self):
        return f"{self.username} - {self.token}"
    
    @property
    def is_authenticated(self):
        return True