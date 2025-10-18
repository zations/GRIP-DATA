from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.CharField(max_length=50, null=False, blank=False)  # tighten constraint

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True, default="")
