from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)

class Snippet(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE,null=True)