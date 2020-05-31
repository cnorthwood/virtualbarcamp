from django.contrib.auth import views as authviews
from django.urls import path

from virtualbarcamp.accounts.views import login, accept_code_of_conduct

urlpatterns = [
    path("code-of-conduct/", accept_code_of_conduct, name="accept_code_of_conduct"),
    path("login/", login, name="login"),
    path("logout/", authviews.logout_then_login, name="logout"),
]
