from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = "virtualbarcamp.home"

    def ready(self):
        import virtualbarcamp.home.signals
