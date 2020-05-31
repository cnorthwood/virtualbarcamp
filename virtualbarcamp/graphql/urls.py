from django.conf import settings
from django.urls import path

from virtualbarcamp.graphql.schema import schema
from virtualbarcamp.graphql.views import LoggedInGraphQLView

urlpatterns = [
    path("", LoggedInGraphQLView.as_view(graphiql=settings.DEBUG, schema=schema)),
]
