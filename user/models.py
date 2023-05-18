from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    image = models.ImageField(upload_to='images/', null=True, max_length=255)
    bio = models.CharField(null=False, blank=True, default='', max_length=255)
    owner = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='files/', null=True, max_length=255)


