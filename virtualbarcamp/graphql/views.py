from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView


class LoggedInGraphQLView(LoginRequiredMixin, GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if settings.DEBUG:
            response._csp_update = {
                "style-src": ["'unsafe-inline'", "cdn.jsdelivr.net"],
                "script-src": ["'self'", "cdn.jsdelivr.net"],
            }
        return response
