from graphene import Schema, ObjectType

from virtualbarcamp.graphql.mutations.discord import DiscordMutation
from virtualbarcamp.graphql.queries.global_settings import GlobalSettingsQuery
from virtualbarcamp.graphql.subscriptions.global_settings import GlobalSettingsSubscription


class Query(GlobalSettingsQuery, ObjectType):
    pass


class Mutation(DiscordMutation, ObjectType):
    pass


class Subscription(GlobalSettingsSubscription, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)
