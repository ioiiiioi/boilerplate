from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """
    Custom user model that extends the AbstractUser class.
    """
    # Add any additional fields or methods you need for your custom user model
    # For example, you can add a profile picture field:
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username