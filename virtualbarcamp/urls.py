from django.contrib import admin
from django.urls import path, include

from virtualbarcamp.home.views import home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("graphql/", include("virtualbarcamp.graphql.urls")),
    path("accounts/", include("virtualbarcamp.accounts.urls")),
    path("accounts/social-auth/", include("social_django.urls", namespace="social")),
]
