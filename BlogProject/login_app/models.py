from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user_profile_pictures')
    about = models.TextField(max_length=101, default=' ')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    