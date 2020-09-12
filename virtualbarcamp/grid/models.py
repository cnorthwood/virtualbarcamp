from django.contrib.auth.models import User
from django.db.models import (
    Model,
    CharField,
    ManyToManyField,
    ForeignKey,
CASCADE,
    SET_NULL,
    DateTimeField,
    OneToOneField,
    TextField,
    BooleanField,
)
from django_celery_beat.models import PeriodicTask, ClockedSchedule


class Room(Model):
    room_name = CharField(max_length=32)
    slots = ManyToManyField("Session", through="Slot")
    discord_presenter_role_id = CharField(max_length=20, blank=True)
    discord_category_id = CharField(max_length=20, blank=True)
    discord_presentation_channel_id = CharField(max_length=20, blank=True)
    discord_discussion_channel_id = CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Room: {self.room_name}"


class Session(Model):
    session_name = CharField(max_length=32)
    start_time = DateTimeField()
    end_time = DateTimeField()
    event = TextField(blank=True)

    def __str__(self):
        return f"Session: {self.session_name}"


class Slot(Model):
    room = ForeignKey(Room, on_delete=CASCADE)
    session = ForeignKey(Session, on_delete=CASCADE)
    slot_start_scheduled_action = ForeignKey(
        PeriodicTask, on_delete=SET_NULL, blank=True, null=True, related_name="+"
    )
    slot_end_scheduled_action = ForeignKey(
        PeriodicTask, on_delete=SET_NULL, blank=True, null=True, related_name="+"
    )

    def sync_scheduled_action_timings(self):
        if not self.slot_start_scheduled_action:
            self.slot_start_scheduled_action = PeriodicTask.objects.create(
                name=f"Start {str(self)}",
                task="virtualbarcamp.grid.tasks.slot_starts",
                clocked=ClockedSchedule.objects.create(clocked_time=self.session.start_time),
                args=[self.id],
                one_off=True,
            )
        else:
            self.slot_start_scheduled_action.name = f"Start {str(self)}"
            self.slot_start_scheduled_action.save()
            self.slot_start_scheduled_action.clocked.clocked_time = self.session.start_time
            self.slot_start_scheduled_action.clocked.save()

        if not self.slot_end_scheduled_action:
            self.slot_end_scheduled_action = PeriodicTask.objects.create(
                name=f"End {self}",
                task="virtualbarcamp.grid.tasks.slot_ends",
                clocked=ClockedSchedule.objects.create(clocked_time=self.session.end_time),
                args=[self.id],
                one_off=True,
            )
        else:
            self.slot_end_scheduled_action.name = f"End {str(self)}"
            self.slot_end_scheduled_action.save()
            self.slot_end_scheduled_action.clocked.clocked_time = self.session.end_time
            self.slot_end_scheduled_action.clocked.save()

    def __str__(self):
        return f"Slot: {self.session.session_name} / {self.room.room_name}"


class Talk(Model):
    slot = OneToOneField(Slot, on_delete=CASCADE)
    title = TextField()
    owner = ForeignKey(User, on_delete=CASCADE)
    open_discussion = BooleanField(default=False)
    other_speakers = ManyToManyField(User, related_name="+", blank=True)

    def __str__(self):
        return f"Talk: {self.title}"
