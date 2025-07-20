import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from address.models import Region, Province, City_Municipality, Barangay

def unique_profile_image_name(instance, filename):
    # Generate a random UUID and append to filename
    ext = filename.split('.')[-1]
    new_filename = f"{instance.user.id}_{uuid.uuid4()}.{ext}"
    return os.path.join('profile_images', new_filename)

class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHERS = 'O'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    ]

    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=OTHERS)
    image = models.ImageField(upload_to=unique_profile_image_name, default='default_profile_image.jpg')
    location = models.CharField(max_length=100, blank=True)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True)
    city_municipality = models.ForeignKey(City_Municipality, on_delete=models.SET_NULL, null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower_id', on_delete=models.CASCADE)
    leader = models.ForeignKey(User, related_name='leader_id', on_delete=models.CASCADE)

    def __str__(self):
        return self.leader.username