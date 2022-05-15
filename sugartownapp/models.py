import email
from email.policy import default
import uuid
from django.db import models
from sqlalchemy import false
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class UserProfile(models.Model):
    username = models.CharField(max_length=1024, null=False,
                                unique=False, primary_key=True, default="")
    name = models.CharField(max_length=1024, null=False,
                            unique=False, default="")
    email = models.EmailField(
        max_length=1024, null=False, unique=True, default="")
    contact = models.CharField(
        max_length=12, null=False, unique=True, default="")
    head_shot = models.ImageField(
        upload_to='user_face_images/', blank=True, default="")

    def __str__(self):
        return self.username


class userfaceid(models.Model):
    id_face = models.AutoField(primary_key=True, default=0)
    username = models.CharField(
        max_length=1024, null=False, unique=True, default="")

    def __str__(self):
        return self.id_face
