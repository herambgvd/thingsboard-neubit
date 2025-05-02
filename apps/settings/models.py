import uuid

from django.db import models

from apps.teams.models import BaseTeamModel


# Create your models here.

class IotConfig(BaseTeamModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=2000, null=True, blank=True)
    refresh_token = models.CharField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = "IOT Config"
        verbose_name_plural = "IOT Configs"


class TeamProfileImage(BaseTeamModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    image = models.ImageField(upload_to="team_profile_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = "Team Profile Image"
        verbose_name_plural = "Team Profile Images"