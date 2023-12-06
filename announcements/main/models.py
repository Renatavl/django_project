from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class Announcement(models.Model):
    ACCESS_CHOICES = (
        ('public', 'Public'),
        ('local', 'Local'),
    )

    subject = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    access = models.CharField(max_length=6, choices=ACCESS_CHOICES, default='public')
    location = models.CharField(max_length=255, blank=True, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
