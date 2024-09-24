from django.db import models
from user_auth.models import LoginUser
from app_recipe.constants import CATEGORY_CHOICES




class Recipe(models.Model):
    user = models.ForeignKey(LoginUser, on_delete=models.CASCADE, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    ingredients = models.TextField()
    method = models.TextField()
    
    
    def __str__(self):
        return self.name
    