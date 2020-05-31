from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from graphene_django.views import GraphQLView


class LoggedInGraphQLView(UserPassesTestMixin, GraphQLView):
    def test_func(self):
        return (
            hasattr(self.request.user, "account")
            and self.request.user.account.has_accepted_code_of_conduct is not None
        )

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if settings.DEBUG:
            response._csp_update = {
                "style-src": ["'unsafe-inline'", "cdn.jsdelivr.net"],
                "script-src": ["'self'", "cdn.jsdelivr.net"],
            }
        return response
