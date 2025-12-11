from django.db import models
from django.contrib.auth.models import User

# Extend default Django User using Profile model
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('poster', 'Task Poster'),
        ('freelancer', 'Freelancer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.png')
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
