from django.contrib.auth import User
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    GENDER_CHOICE = (
        ('Male' , "Male"),
        ('Female', "Female"),
    )
    gender = models.CharField(choices=GENDER_CHOICE, max_length=20, null=True)
    birthdate = models.DateField(null=True)

    def __str__(self):
        return  f"{self.user.username}'s Profile"
