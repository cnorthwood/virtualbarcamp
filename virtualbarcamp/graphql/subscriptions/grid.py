from graphene import ObjectType, NonNull

from virtualbarcamp.graphql.queries.grid import SlotType


class GridSubscription(ObjectType):
    slotChanged = NonNull(SlotType)
