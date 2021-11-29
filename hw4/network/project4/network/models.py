from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
    body = models.CharField(max_length=255)

    def __str__(self):
        return f"From {self.poster}: {self.body}"