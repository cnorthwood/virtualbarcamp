from django.urls import path

from virtualbarcamp.home.views import home_view

urlpatterns = [path("", home_view, name="home")]
