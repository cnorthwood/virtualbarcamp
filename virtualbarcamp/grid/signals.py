from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from virtualbarcamp.grid.models import Talk

post_save.connect(post_save_subscription, sender=Talk, dispatch_uid="grid_update")
post_delete.connect(post_delete_subscription, sender=Talk, dispatch_uid="grid_talk_clear")
