from celery import shared_task

from virtualbarcamp.home.models import GlobalSettings, EventState


@shared_task()
def open_doors():
    settings = GlobalSettings.objects.first()
    settings.event_state = EventState.DOORS_OPEN
    settings.save()


@shared_task
def open_grid():
    settings = GlobalSettings.objects.first()
    settings.event_state = EventState.GRID_OPEN
    settings.save()


@shared_task
def close_event():
    settings = GlobalSettings.objects.first()
    settings.event_state = EventState.POST_EVENT
    settings.save()
