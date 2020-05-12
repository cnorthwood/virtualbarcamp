from django.contrib import admin

from virtualbarcamp.home.models import GlobalSettings


@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
