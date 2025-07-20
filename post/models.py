import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def unique_post_image_name(instance, filename):
    # Generate a random UUID and append to filename
    ext = filename.split('.')[-1]
    new_filename = f"{instance.created_by.id}_{uuid.uuid4()}.{ext}"
    return os.path.join('post_images', new_filename)

class Post(models.Model):
    caption = models.TextField()
    image = models.ImageField(upload_to=unique_post_image_name)
    no_of_likes = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.created_by.username
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.created_by.username
    
class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.created_by.username