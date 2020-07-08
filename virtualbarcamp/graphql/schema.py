from graphene import Schema, ObjectType

from virtualbarcamp.graphql.mutations.discord import DiscordMutation
from virtualbarcamp.graphql.mutations.grid import GridMutation
from virtualbarcamp.graphql.queries.discord import DiscordQuery
from virtualbarcamp.graphql.queries.global_settings import GlobalSettingsQuery
from virtualbarcamp.graphql.queries.grid import GridQuery
from virtualbarcamp.graphql.subscriptions.global_settings import GlobalSettingsSubscription
from virtualbarcamp.graphql.subscriptions.grid import GridSubscription


class Query(DiscordQuery, GlobalSettingsQuery, GridQuery, ObjectType):
    pass


class Mutation(DiscordMutation, GridMutation, ObjectType):
    pass


class Subscription(GlobalSettingsSubscription, GridSubscription, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)
