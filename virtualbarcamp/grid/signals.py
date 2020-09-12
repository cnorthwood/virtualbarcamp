from django.conf import settings
from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from virtualbarcamp.discord import sync_channels, delete_channels
from virtualbarcamp.grid.models import Talk, Room, Slot, Session


def save_room(sender, instance: Room, **kwargs):
    if getattr(instance, "_synced", False):
        return

    if not settings.DISCORD_SYNC_DISABLED:
        sync_channels(instance)
    instance._synced = True
    instance.save()


def delete_room(sender, instance: Room, **kwargs):
    if not settings.DISCORD_SYNC_DISABLED:
        delete_channels(instance)


def save_slot(sender, instance: Slot, **kwargs):
    if getattr(instance, "_synced", False):
        return

    if not settings.DISCORD_SYNC_DISABLED:
        instance.sync_scheduled_action_timings()

    instance._synced = True
    instance.save()


def delete_slot(sender, instance: Slot, **kwargs):
    instance.slot_start_scheduled_action.delete()
    instance.slot_end_scheduled_action.delete()


def save_session(sender, instance: Session, **kwargs):
    for slot in instance.slot_set.all():
        slot.sync_scheduled_action_timings()
        slot._synced = True
        slot.save()


post_save.connect(save_room, sender=Room)
post_delete.connect(delete_room, sender=Room)
post_save.connect(post_save_subscription, sender=Talk, dispatch_uid="grid_update")
post_delete.connect(post_delete_subscription, sender=Talk, dispatch_uid="grid_talk_clear")
post_save.connect(save_session, sender=Session)
post_save.connect(save_slot, sender=Slot)
post_delete.connect(delete_slot, sender=Slot)
