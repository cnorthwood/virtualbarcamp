from datetime import datetime

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from graphene import ObjectType, Field, NonNull, ID, String, List, Boolean
from pytz import utc

from virtualbarcamp.graphql.queries.grid import SlotType, TalkType
from virtualbarcamp.grid.models import Talk, Slot
from virtualbarcamp.home.models import GlobalSettings


class GridMutation(ObjectType):
    remove_talk = Field(NonNull(SlotType), slot_id=NonNull(ID))
    add_talk = Field(
        NonNull(SlotType),
        slot_id=NonNull(ID),
        title=NonNull(String),
        additional_speakers=NonNull(List(NonNull(ID))),
        is_open_discussion=NonNull(Boolean),
    )
    move_talk = Field(
        NonNull(List(NonNull(SlotType))),
        talk_id=NonNull(ID),
        to_slot=NonNull(ID),
    )
    update_talk = Field(
        NonNull(TalkType),
        talk_id=NonNull(ID),
        title=NonNull(String),
        additional_speakers=NonNull(List(NonNull(ID))),
        is_open_discussion=NonNull(Boolean),
    )

    @staticmethod
    def resolve_remove_talk(parent, info, slot_id):
        global_settings = GlobalSettings.objects.first()
        if global_settings.event_state not in ("GRID_OPEN",):
            raise ValueError("Can not remove talks when grid is not open")

        slot = Slot.objects.get(id=slot_id)
        if info.context.user != slot.talk.owner:
            raise ValueError("Not authorised")

        if slot.session.end_time < datetime.now(tz=utc):
            raise ValueError("Session has already ended")

        slot.talk.delete()
        slot.refresh_from_db()

        return slot

    @staticmethod
    def resolve_add_talk(parent, info, slot_id, title, additional_speakers, is_open_discussion):
        global_settings = GlobalSettings.objects.first()
        if global_settings.event_state not in ("GRID_OPEN",):
            raise ValueError("Can not add talks when grid is not open")

        if Slot.objects.get(id=slot_id).session.end_time < datetime.now(tz=utc):
            raise ValueError("Session has already ended")

        with transaction.atomic():
            try:
                talk = Talk.objects.create(
                    slot_id=slot_id,
                    title=title,
                    open_discussion=is_open_discussion,
                    owner=info.context.user,
                )
            except IntegrityError:
                raise ValueError("This slot already has a talk")
            else:
                talk.other_speakers.set(
                    User.objects.filter(
                        id__in=(int(speaker_id) for speaker_id in additional_speakers)
                    )
                )
                return talk.slot

    @staticmethod
    def resolve_move_talk(parent, info, talk_id, to_slot):
        global_settings = GlobalSettings.objects.first()
        if global_settings.event_state not in ("GRID_OPEN",):
            raise ValueError("Can not move talks when grid is not open")

        talk = Talk.objects.get(id=talk_id)
        if info.context.user != talk.owner:
            raise ValueError("Not authorised")

        if talk.slot.session.start_time < datetime.now(tz=utc):
            raise ValueError("Talk has already started")

        old_slot = talk.slot
        talk.slot_id = to_slot
        with transaction.atomic():
            try:
                talk.save()
            except IntegrityError:
                raise ValueError("Landing slot is already full")
        return [old_slot, talk.slot]

    @staticmethod
    def resolve_update_talk(parent, info, talk_id, title, additional_speakers, is_open_discussion):
        global_settings = GlobalSettings.objects.first()
        if global_settings.event_state not in ("GRID_OPEN",):
            raise ValueError("Can not update talks when grid is not open")

        talk = Talk.objects.get(id=talk_id)
        if info.context.user != talk.owner:
            raise ValueError("Not authorised")

        if talk.slot.session.end_time < datetime.now(tz=utc):
            raise ValueError("Session has already ended")

        talk.title = title
        talk.open_discussion = is_open_discussion
        talk.other_speakers.set(
            User.objects.filter(id__in=(int(speaker_id) for speaker_id in additional_speakers))
        )
        talk.save()
        return talk
