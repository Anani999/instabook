from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    bio = models.TextField(null=True)
    profile_image = models.ImageField(upload_to='profile_images/',default='profile_images/default.jpg')

    def __str__(self) -> str:
        return super().__str__()

    