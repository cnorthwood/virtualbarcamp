from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from virtualbarcamp.discord import remove_from_server


@receiver(post_save, sender=User)
def remove_user_from_discord_if_disabled(instance: User, **kwargs):
    if not instance.is_active:
        remove_from_server(instance)
