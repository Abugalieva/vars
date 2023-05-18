from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(null=False, max_length=255)
    description = models.TextField(null=False, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class Post(models.Model):
    title = models.CharField(null=False, max_length=255)
    content = models.CharField(null=False, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=False, related_name='posts')
    image = models.ImageField(upload_to='images/', null=True, max_length=255)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'



