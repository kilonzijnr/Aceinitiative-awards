from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Profile(models.Model):
    """model for user profile"""
    profile_pic = CloudinaryField("image")
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=70, blank=True)
    email= models.EmailField()
    bio = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    def save_profile(self):
        self.save()