from django.db.models.signals import post_save
from graphene_subscriptions.signals import post_save_subscription

from virtualbarcamp.home.models import GlobalSettings

post_save.connect(
    post_save_subscription, sender=GlobalSettings, dispatch_uid="global_settings_update"
)
