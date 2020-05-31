from django.contrib.auth import views as authviews
from django.urls import path

from virtualbarcamp.accounts.views import login

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", authviews.logout_then_login, name="logout"),
]
