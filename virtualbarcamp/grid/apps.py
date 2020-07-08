from django.apps import AppConfig


class GridConfig(AppConfig):
    name = "virtualbarcamp.grid"

    def ready(self):
        import virtualbarcamp.grid.signals
