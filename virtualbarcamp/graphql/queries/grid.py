from django.contrib.auth.models import User
from graphene import ObjectType, NonNull, List, String, DateTime, ID, Boolean, Field

from virtualbarcamp.grid.models import Session, Room, Talk
from virtualbarcamp.home.models import GlobalSettings


class SpeakerType(ObjectType):
    class Meta:
        name = "Speaker"

    id = NonNull(ID)
    name = NonNull(String)

    @staticmethod
    def resolve_name(parent: User, info):
        return parent.username


class TalkType(ObjectType):
    class Meta:
        name = "Talk"

    id = NonNull(ID)
    title = NonNull(String)
    speakers = NonNull(List(NonNull(SpeakerType)))
    is_open_discussion = NonNull(Boolean)
    is_mine = NonNull(Boolean)

    @staticmethod
    def resolve_speakers(parent: Talk, info):
        return [parent.owner] + parent.other_speakers

    @staticmethod
    def resolve_is_open_discussion(parent: Talk, info):
        return parent.open_discussion

    @staticmethod
    def resolve_is_mine(parent: Talk, info):
        return parent.owner == info.context.user


class RoomType(ObjectType):
    class Meta:
        name = "Room"

    id = NonNull(ID)
    name = NonNull(String)
    slots = NonNull(List(NonNull(lambda: SlotType)))

    @staticmethod
    def resolve_name(parent: Room, info):
        return parent.room_name

    @staticmethod
    def resolve_slots(parent: Room, info):
        return parent.slot_set.all()


class SlotType(ObjectType):
    class Meta:
        name = "Slot"

    id = NonNull(ID)
    talk = Field(TalkType)
    session = NonNull(lambda: SessionType)
    room = NonNull(RoomType)


class SessionType(ObjectType):
    class Meta:
        name = "Session"

    id = NonNull(ID)
    name = NonNull(String)
    start_time = NonNull(DateTime)
    end_time = NonNull(DateTime)
    event = String()
    rooms = NonNull(List(NonNull(RoomType)))
    slots = List(NonNull(SlotType))

    @staticmethod
    def resolve_name(parent: Session, info):
        return parent.session_name

    @staticmethod
    def resolve_event(parent: Session, info):
        if parent.event == "":
            return None
        else:
            return parent.event

    @staticmethod
    def resolve_rooms(parent: Session, info):
        return (slot.room for slot in parent.slot_set.all())

    @staticmethod
    def resolve_slots(parent: Session, info):
        return parent.slot_set.all()


class GridType(ObjectType):
    class Meta:
        name = "Grid"

    sessions = NonNull(List(NonNull(SessionType)))

    @staticmethod
    def resolve_sessions(parent, info):
        return parent["sessions"].order_by("start_time")


class GridQuery(ObjectType):
    grid = NonNull(GridType)
    speakers = NonNull(List(NonNull(SpeakerType)))

    @staticmethod
    def resolve_grid(parent, info):
        global_settings = GlobalSettings.objects.first()
        if global_settings.event_state in ("GRID_OPEN",):
            return {"sessions": Session.objects.all()}
        else:
            raise ValueError("Can not view grid in this state")
