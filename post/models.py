from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from user_profile.models import Profile
import uuid

# class Post(models.Model):
#     caption = models.TextField()
#     image = models.ImageField(upload_to='post_images')
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=datetime.now)

#     def __str__(self):
#         return self.created_by.username
    
# class Like(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=datetime.now)

#     def __str__(self):
#         return self.created_by.username
    
# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=datetime.now)

#     def __str__(self):
#         return self.created_by.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    profile = models.ForeignKey(Profile, related_name='profile_id_post', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    username = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, related_name='profile_id_like_post', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_id_like_post', on_delete=models.CASCADE)

    def __str__(self):
        return self.username