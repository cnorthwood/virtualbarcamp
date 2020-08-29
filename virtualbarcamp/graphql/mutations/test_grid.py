from datetime import datetime

from django.contrib.auth.models import User
import pytest
from pytz import utc

from virtualbarcamp.graphql.mutations.grid import GridMutation
from virtualbarcamp.graphql.testutils import GraphQLInfo
from virtualbarcamp.grid.models import Talk, Slot, Session, Room
from virtualbarcamp.home.models import GlobalSettings, EventState


def _create_slot():
    room = Room.objects.create(room_name="Where it happens")
    session = Session.objects.create(
        session_name="Talks",
        start_time=datetime(2020, 1, 1, 12, 0, 0, tzinfo=utc),
        end_time=datetime(2020, 1, 1, 12, 30, 0, tzinfo=utc),
    )
    return Slot.objects.create(room=room, session=session)


def _create_talk(**kwargs):
    return Talk.objects.create(slot=_create_slot(), **kwargs)


def _set_global_settings(state):
    global_settings, _ = GlobalSettings.objects.get_or_create(id=1)
    global_settings.event_state = state
    global_settings.save()


@pytest.mark.django_db
def test_updating_a_talk_fails_unless_grid_is_open():
    _set_global_settings(EventState.DOORS_OPEN)
    user = User.objects.create(username="user1")
    talk = _create_talk(owner=user, title="A talk")

    with pytest.raises(ValueError):
        GridMutation.resolve_update_talk(
            None,
            GraphQLInfo(user),
            talk_id=talk.id,
            title="A new title",
            additional_speakers=[],
            is_open_discussion=True,
        )


@pytest.mark.django_db
def test_updating_a_talk_you_do_not_own_fails():
    _set_global_settings(EventState.GRID_OPEN)
    user = User.objects.create(username="user1")
    owner = User.objects.create(username="user2")
    talk = _create_talk(owner=owner, title="A talk")

    with pytest.raises(ValueError):
        GridMutation.resolve_update_talk(
            None,
            GraphQLInfo(user),
            talk_id=talk.id,
            title="A new title",
            additional_speakers=[],
            is_open_discussion=True,
        )

    talk.refresh_from_db()
    assert talk.title == "A talk"
    assert talk.open_discussion is False


@pytest.mark.django_db
def test_updating_a_talk_you_own():
    _set_global_settings(EventState.GRID_OPEN)
    user = User.objects.create(username="user1")
    speaker = User.objects.create(username="user2")
    talk = _create_talk(owner=user, title="A talk")

    GridMutation.resolve_update_talk(
        None,
        GraphQLInfo(user),
        talk_id=talk.id,
        title="A new title",
        additional_speakers=[speaker.id],
        is_open_discussion=True,
    )

    talk.refresh_from_db()
    assert talk.title == "A new title"
    assert talk.open_discussion is True
    assert [speaker] == list(talk.other_speakers.all())


@pytest.mark.django_db
def test_adding_a_talk_fails_unless_grid_is_open():
    _set_global_settings(EventState.DOORS_OPEN)
    user = User.objects.create(username="user1")
    slot = _create_slot()

    with pytest.raises(ValueError):
        GridMutation.resolve_add_talk(
            None,
            GraphQLInfo(user),
            slot_id=slot.id,
            title="A new title",
            additional_speakers=[],
            is_open_discussion=True,
        )


@pytest.mark.django_db
def test_adding_a_talk_succeeds_grid_is_open():
    _set_global_settings(EventState.GRID_OPEN)
    user = User.objects.create(username="user1")
    speaker = User.objects.create(username="user2")
    slot = _create_slot()

    talk_slot = GridMutation.resolve_add_talk(
        None,
        GraphQLInfo(user),
        slot_id=slot.id,
        title="A new title",
        additional_speakers=[speaker.id],
        is_open_discussion=True,
    )

    assert talk_slot == slot
    assert talk_slot.talk.title == "A new title"
    assert talk_slot.talk.open_discussion is True
    assert talk_slot.talk.owner == user
    assert [speaker] == list(talk_slot.talk.other_speakers.all())


@pytest.mark.django_db
def test_adding_a_talk_fails_when_slot_is_already_in_use():
    _set_global_settings(EventState.GRID_OPEN)
    user = User.objects.create(username="user1")
    talk = _create_talk(owner=user, title="A talk")

    with pytest.raises(ValueError):
        GridMutation.resolve_add_talk(
            None,
            GraphQLInfo(user),
            slot_id=talk.slot.id,
            title="A new title",
            additional_speakers=[],
            is_open_discussion=True,
        )

    talk.refresh_from_db()

    assert talk.slot.talk == talk


@pytest.mark.django_db
def test_moving_a_talk_fails_unless_grid_is_open():
    _set_global_settings(EventState.DOORS_OPEN)
    user = User.objects.create(username="user1")
    talk = _create_talk(owner=user, title="A talk")
    slot = _create_slot()

    with pytest.raises(ValueError):
        GridMutation.resolve_move_talk(None, GraphQLInfo(user), talk_id=talk.id, to_slot=slot.id)


@pytest.mark.django_db
def test_moving_a_talk_fails_unless_user_owns_it():
    _set_global_settings(EventState.GRID_OPEN)
    user = User.objects.create(username="user1")
    other_user = User.objects.create(username="user2")
    talk = _create_talk(owner=other_user, title="A talk")
    slot = _create_slot()

    with pytest.raises(ValueError):
        GridMutation.resolve_move_talk(None, GraphQLInfo(user), talk_id=talk.id, to_slot=slot.id)


@pytest.mark.django_db
def test_moving_a_talk_fails_unless_landing_slot_is_clear():
    _set_global_settings(EventState.GRID_OPEN)
    user = User.objects.create(username="user1")
    talk = _create_talk(owner=user, title="A talk")
    other_talk = _create_talk(owner=user, title="A talk")

    with pytest.raises(ValueError):
        GridMutation.resolve_move_talk(
            None, GraphQLInfo(user), talk_id=talk.id, to_slot=other_talk.slot_id
        )


@pytest.mark.django_db
def test_moving_a_talk_succeeds():
    _set_global_settings(EventState.GRID_OPEN)
    user = User.objects.create(username="user1")
    talk = _create_talk(owner=user, title="A talk")
    slot = _create_slot()

    GridMutation.resolve_move_talk(None, GraphQLInfo(user), talk_id=talk.id, to_slot=slot.id)

    slot.refresh_from_db()
    assert slot.talk == talk


@pytest.mark.django_db
def test_removing_a_talk_fails_unless_grid_is_open():
    _set_global_settings(EventState.DOORS_OPEN)
    user = User.objects.create(username="user1")
    talk = _create_talk(owner=user, title="A talk")

    with pytest.raises(ValueError):
        GridMutation.resolve_remove_talk(
            None,
            GraphQLInfo(user),
            slot_id=talk.slot.id,
        )


@pytest.mark.django_db
def test_removing_a_talk_fails_unless_user_owns_it():
    _set_global_settings(EventState.GRID_OPEN)
    user = User.objects.create(username="user1")
    other_user = User.objects.create(username="user2")
    talk = _create_talk(owner=other_user, title="A talk")

    with pytest.raises(ValueError):
        GridMutation.resolve_remove_talk(
            None,
            GraphQLInfo(user),
            slot_id=talk.slot.id,
        )


@pytest.mark.django_db
def test_removing_a_talk_succeeds():
    _set_global_settings(EventState.GRID_OPEN)
    user = User.objects.create(username="user1")
    talk = _create_talk(owner=user, title="A talk")

    slot = GridMutation.resolve_remove_talk(
        None,
        GraphQLInfo(user),
        slot_id=talk.slot.id,
    )

    with pytest.raises(Slot.talk.RelatedObjectDoesNotExist):
        assert slot.talk is None
    with pytest.raises(Talk.DoesNotExist):
        Talk.objects.get(id=talk.id)
