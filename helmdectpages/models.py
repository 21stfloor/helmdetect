from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Remove the username field entirely
    username = None

    email = models.EmailField(unique=True)
    # Add other fields as needed

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
        
        