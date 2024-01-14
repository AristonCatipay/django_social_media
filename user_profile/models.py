from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHERS = 'O'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'O'),
    ]

    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=OTHERS)
    image = models.ImageField(upload_to='profile_images', default='default_profile_image.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# class Follow(models.Model):
#     follower = models.ForeignKey(User, related_name='follower_id', on_delete=models.CASCADE)
#     leader = models.ForeignKey(User, related_name='leader_id', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.leader.username

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     id_user = models.IntegerField()
#     bio = models.TextField(blank=True)
#     profile_image = models.ImageField(upload_to='profile_images', default='default_profile_image.jpg')
#     location = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return self.user.username
    
class Followers(models.Model):
    follower_username = models.CharField(max_length=100)
    leader_username = models.CharField(max_length=100)
    follower = models.ForeignKey(User, related_name='follower_id', on_delete=models.CASCADE)
    leader = models.ForeignKey(User, related_name='leader_id', on_delete=models.CASCADE)

    def __str__(self):
        return self.leader_username