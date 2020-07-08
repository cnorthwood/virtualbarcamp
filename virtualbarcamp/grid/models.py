from django.contrib.auth.models import User
from django.db.models import (
    Model,
    CharField,
    ManyToManyField,
    ForeignKey,
    CASCADE,
    DateTimeField,
    OneToOneField,
    TextField,
    BooleanField,
)


class Room(Model):
    room_name = CharField(max_length=32)
    slots = ManyToManyField("Session", through="Slot")


class Session(Model):
    session_name = CharField(max_length=32)
    start_time = DateTimeField()
    end_time = DateTimeField()
    event = TextField(blank=True)


# TODO: wire up model changes to Celery events
class Slot(Model):
    room = ForeignKey(Room, on_delete=CASCADE)
    session = ForeignKey(Session, on_delete=CASCADE)


class Talk(Model):
    slot = OneToOneField(Slot, on_delete=CASCADE)
    title = TextField()
    owner = ForeignKey(User, on_delete=CASCADE)
    open_discussion = BooleanField(default=False)
    other_speakers = ManyToManyField(User, related_name="+")
