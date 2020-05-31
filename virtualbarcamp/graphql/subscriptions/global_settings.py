from graphene import ObjectType, NonNull

from virtualbarcamp.graphql.queries.global_settings import GlobalSettingsType
from virtualbarcamp.home.models import GlobalSettings


class GlobalSettingsSubscription(ObjectType):
    global_settings = NonNull(GlobalSettingsType)

    @staticmethod
    def resolve_global_settings(parent, info):
        return parent.filter(lambda event: isinstance(event.instance, GlobalSettings)).map(
            lambda event: event.instance
        )
