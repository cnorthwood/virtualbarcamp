from graphene import ObjectType, Field, NonNull, Boolean

from virtualbarcamp.discord import invite_to_server
from virtualbarcamp.home.models import GlobalSettings


class DiscordMutation(ObjectType):
    invite_to_discord = Field(NonNull(Boolean))

    @staticmethod
    def resolve_invite_to_discord(parent, info):
        global_settings = GlobalSettings.objects.first()
        if global_settings.event_state in ("DOORS_OPEN", "GRID_OPEN"):
            return invite_to_server(info.context.user)
        else:
            raise ValueError("Can not invite to Discord in this state")
