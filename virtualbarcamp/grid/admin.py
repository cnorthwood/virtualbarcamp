from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField

from virtualbarcamp.grid.models import Room, Session, Slot, Talk


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


class SessionForm(ModelForm):
    rooms = ModelMultipleChoiceField(queryset=Room.objects.all(), required=False)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    form = SessionForm

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if obj:
            form.base_fields["rooms"].initial = [slot.room for slot in obj.slot_set.all()]
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        rooms = set(form.cleaned_data.get("rooms"))
        for slot in obj.slot_set.all():
            if slot.room not in rooms:
                slot.delete()
        current_rooms = {slot.room for slot in obj.slot_set.all()}
        for room in rooms:
            if room not in current_rooms:
                obj.slot_set.create(room=room)


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    pass


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    pass
