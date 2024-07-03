from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    bio = models.TextField(null=True)
    profile_image = models.ImageField(upload_to='profile_images/',default='profile_images/default.jpg')

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.TextField()
    image = models.ImageField(upload_to='post_images/',null=True,blank=True)
    video = models.FileField(upload_to='post_videos/',null=True,blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.user.username} : {self.caption}")

class Likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return (f"{self.user.username} : {self.post.caption}")

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return (f"{self.user.username} : {self.post.caption}")


class Share(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return (f"{self.user.username} : {self.post.caption}")

class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.follower.username} => {self.following.username}"