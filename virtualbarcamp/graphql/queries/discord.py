from graphene import ObjectType, Boolean, NonNull

from virtualbarcamp.discord import is_on_server


class DiscordQuery(ObjectType):
    is_on_discord = NonNull(Boolean)

    @staticmethod
    def resolve_is_on_discord(parent, info):
        return is_on_server(info.context.user)

