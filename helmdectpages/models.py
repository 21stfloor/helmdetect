from django.db import models
from django.contrib.auth.models import AbstractUser

from helmdectpages.managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Add other fields as needed

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    # Add other fields as needed
# Create your models here.
class FirebaseModel(models.Model):
    class Meta:
        app_label = 'helmdectpages'
        db_table = 'helmdectpages_firebase'
        managed = False
        
# class User(models.Model):
#     email = models.EmailField(max_length=100)
#     password = models.CharField(max_length=100)
    
    
#     def __str__(self):
#         return self.email
        
        