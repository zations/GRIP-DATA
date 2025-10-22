from django.db import models
from django.db.models import Q

class NoteQuerySet(models.QuerySet):
    def search(self, q):
        return self.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(tag__icontains=q)
        )
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.CharField(max_length=50, null=False, blank=False)  # tighten constraint

    created_at = models.DateTimeField(auto_now_add=True)
    objects = NoteQuerySet.as_manager()   # ✅ fixed manager and added helper
    
    class Meta:
        ordering = ["-created_at"]                # newest notes first
        indexes = [models.Index(fields=["tag"])]  # speeds up tag-based queries
    def __str__(self):
        return self.title

from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True, default="")
