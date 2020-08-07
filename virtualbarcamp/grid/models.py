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
