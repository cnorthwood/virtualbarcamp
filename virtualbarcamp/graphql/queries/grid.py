from graphene import ObjectType, NonNull, List, String, DateTime, ID, Boolean


class SpeakerType(ObjectType):
    class Meta:
        name = "Speaker"

    id = NonNull(ID)
    name = NonNull(String)


class TalkType(ObjectType):
    class Meta:
        name = "Talk"

    id = NonNull(ID)
    title = NonNull(String)
    speakers = NonNull(List(NonNull(SpeakerType)))
    is_open_discussion = NonNull(Boolean)
    is_mine = NonNull(Boolean)


class SlotType(ObjectType):
    class Meta:
        name = "Slot"

    id = NonNull(ID)
    talk = TalkType()


class SessionType(ObjectType):
    class Meta:
        name = "Session"

    id = NonNull(ID)
    session_name = NonNull(String)
    start_time = NonNull(DateTime)
    end_time = NonNull(DateTime)
    event = String()
    slots = List(NonNull(SlotType))


class GridType(ObjectType):
    class Meta:
        name = "Grid"

    sessions = NonNull(List(NonNull(SessionType)))


class GridQuery(ObjectType):
    grid = NonNull(GridType)
    speakers = NonNull(List(NonNull(SpeakerType)))
