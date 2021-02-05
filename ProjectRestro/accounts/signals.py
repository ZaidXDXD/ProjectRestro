from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save

from .models import Profile


def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="customer")
        instance.groups.add(group)
        Profile.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )
        print("Profile Created!")

post_save.connect(customer_profile, sender=User)
