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

class Project(models.Model):
    """Class model for the project fields"""
    projectimage = CloudinaryField("image", null=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.CharField(max_length=150)
    

    def __str__(self):
        return self.name

    def save_project(self):
        self.save()
        
    @classmethod
    def search_by_name(cls, search_term):
        """Class method to source a project"""
        projects = cls.objects.filter(name_icontains = search_term)
        return projects