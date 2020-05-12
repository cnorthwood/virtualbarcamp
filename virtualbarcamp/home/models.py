from django.db.models import Model, BooleanField


class GlobalSettings(Model):
    class Meta:
        verbose_name = "global settings"
        verbose_name_plural = "global settings"

    allow_registration = BooleanField(default=False)
