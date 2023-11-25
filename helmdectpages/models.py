from django.db import models

# Create your models here.
class FirebaseModel(models.Model):
    class Meta:
        app_label = 'helmdectpages'
        db_table = 'helmdectpages_firebase'
        managed = False
        
class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.email
        
        