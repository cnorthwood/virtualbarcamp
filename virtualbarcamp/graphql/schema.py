from graphene import Schema, ObjectType, Boolean
from rx import Observable

from virtualbarcamp.graphql.queries.global_settings import GlobalSettingsQuery


class Query(GlobalSettingsQuery, ObjectType):
    pass


class Mutation(ObjectType):
    hello_world = Boolean()

    @staticmethod
    def resolve_hello_world(parent, info):
        return True


class Subscription(ObjectType):
    hello_world = Boolean()

    @staticmethod
    def resolve_hello_world(parent, info):
        return Observable.interval(3000).map(lambda i: True)


schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)
