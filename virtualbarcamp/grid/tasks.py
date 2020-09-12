from celery import shared_task
from django.conf import settings

from virtualbarcamp.discord import start_slot, end_slot
from virtualbarcamp.grid.models import Slot


@shared_task
def slot_starts(slot_id):
    slot = Slot.objects.get(id=slot_id)
    if not settings.DISCORD_SYNC_DISABLED:
        start_slot(slot)


@shared_task
def slot_ends(slot_id):
    slot = Slot.objects.get(id=slot_id)
    if not settings.DISCORD_SYNC_DISABLED:
        end_slot(slot)
