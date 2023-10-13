from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', default='default_profile_image.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    profile = models.ForeignKey(Profile, related_name='profile_id_post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    username = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, related_name='profile_id_like_post', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_id_like_post', on_delete=models.CASCADE)

    def __str__(self):
        return self.username
    
class Followers(models.Model):
    follower_username = models.CharField(max_length=100)
    leader_username = models.CharField(max_length=100)

    def __str__(self):
        return self.leader_username