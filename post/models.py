from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Post(models.Model):
    caption = models.TextField()
    image = models.ImageField(upload_to='post_images')
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