from graphene import ObjectType, NonNull, Enum, DateTime

from virtualbarcamp.home.models import GlobalSettings


class EventStateEnum(Enum):
    class Meta:
        name = "EventState"

    PRE_EVENT = "PRE_EVENT"
    DOORS_OPEN = "DOORS_OPEN"
    GRID_OPEN = "GRID_OPEN"
    POST_EVENT = "POST_EVENT"


class GlobalSettingsType(ObjectType):
    class Meta:
        name = "GlobalSettings"

    event_state = NonNull(EventStateEnum)
    doors_open_time = DateTime()
    grid_open_time = DateTime()
    event_close_time = DateTime()


class GlobalSettingsQuery(ObjectType):
    global_settings = NonNull(GlobalSettingsType)

    @staticmethod
    def resolve_global_settings(parent, info):
        return GlobalSettings.objects.first()
