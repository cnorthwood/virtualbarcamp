from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "virtualbarcamp.accounts"

    def ready(self):
        import virtualbarcamp.accounts.signals
