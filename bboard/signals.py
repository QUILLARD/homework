from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from bboard.models import UserProfile


@receiver(post_save, sender=User)
def user_create_or_update(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.userprofile.save()
        except Exception:
            profile = UserProfile(user=instance)
            profile.save()
