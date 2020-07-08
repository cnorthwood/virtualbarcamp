from django.contrib import admin

from virtualbarcamp.grid.models import Room, Session, Slot, Talk


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    pass


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    pass
