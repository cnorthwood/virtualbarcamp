from django.db.models import Model, TextChoices, CharField
from django_celery_beat.models import PeriodicTask

from virtualbarcamp.discord import create_category


class EventState(TextChoices):
    PRE_EVENT = "PRE_EVENT", "pre-event"
    DOORS_OPEN = "DOORS_OPEN", "doors open"
    GRID_OPEN = "GRID_OPEN", "grid open"
    POST_EVENT = "POST_EVENT", "post-event"


class GlobalSettings(Model):
    class Meta:
        verbose_name = "global settings"
        verbose_name_plural = "global settings"

    event_state = CharField(max_length=10, choices=EventState.choices, default=EventState.PRE_EVENT)
    breakout_category_id = CharField(max_length=20, blank=True)

    @property
    def doors_open_time(self):
        return self._task_time("virtualbarcamp.home.tasks.open_doors")

    @property
    def grid_open_time(self):
        return self._task_time("virtualbarcamp.home.tasks.open_grid")

    @property
    def event_close_time(self):
        return self._task_time("virtualbarcamp.home.tasks.close_event")

    def get_or_create_breakout_category_id(self):
        if not self.breakout_category_id:
            self.breakout_category_id = create_category("Breakout Rooms")
            self.save()
        return self.breakout_category_id

    def __str__(self):
        return "Global Settings singleton"

    def _task_time(self, task):
        try:
            return PeriodicTask.objects.get(task=task, enabled=True).clocked.clocked_time
        except PeriodicTask.DoesNotExist:
            return None
