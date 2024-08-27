# comments/models.py
from django.db import models
from accounts.models import CustomUser
from infos.models import Info
from recipes.models import Recipe


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Verknüpfung mit Info und Recipe, optional, da nur eines verwendet wird.
    info = models.ForeignKey(Info, null=True, blank=True, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author} on {self.created_at}"

