from graphene import ObjectType, NonNull

from virtualbarcamp.graphql.queries.grid import SlotType
from virtualbarcamp.grid.models import Talk
from virtualbarcamp.home.models import GlobalSettings


def talk_to_slot(talk: Talk):
    slot = talk.slot
    slot.refresh_from_db()
    return slot


class GridSubscription(ObjectType):
    slot_changed = NonNull(SlotType)

    @staticmethod
    def resolve_slot_changed(parent, info):
        global_settings = GlobalSettings.objects.first()
        if global_settings.event_state not in ("GRID_OPEN",):
            raise ValueError("Can not view grid in this state")
        return parent.filter(lambda event: isinstance(event.instance, Talk)).map(
            lambda event: talk_to_slot(event.instance)
        )
