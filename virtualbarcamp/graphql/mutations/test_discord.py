import pytest
from django.contrib.auth.models import AnonymousUser

from virtualbarcamp.graphql.mutations import discord
from virtualbarcamp.graphql.testutils import GraphQLInfo
from virtualbarcamp.home.models import GlobalSettings, EventState


def _set_global_settings(state):
    global_settings, _ = GlobalSettings.objects.get_or_create(id=1)
    global_settings.event_state = state
    global_settings.save()


@pytest.mark.django_db
def test_inviting_to_discord_is_allowed_when_doors_are_open(mocker):
    mocker.patch("virtualbarcamp.graphql.mutations.discord.invite_to_server")
    discord.invite_to_server.return_value = True
    _set_global_settings(EventState.DOORS_OPEN)

    user = AnonymousUser()
    assert discord.DiscordMutation.resolve_invite_to_discord(None, GraphQLInfo(user)) is True
    discord.invite_to_server.assert_called_once_with(user)


@pytest.mark.django_db
def test_inviting_to_discord_is_allowed_when_grid_is_open(mocker):
    mocker.patch("virtualbarcamp.graphql.mutations.discord.invite_to_server")
    discord.invite_to_server.return_value = True
    _set_global_settings(EventState.GRID_OPEN)

    user = AnonymousUser()
    assert discord.DiscordMutation.resolve_invite_to_discord(None, GraphQLInfo(user)) is True
    discord.invite_to_server.assert_called_once_with(user)


@pytest.mark.django_db
def test_inviting_to_discord_is_not_allowed_when_pre_event(mocker):
    mocker.patch("virtualbarcamp.graphql.mutations.discord.invite_to_server")
    discord.invite_to_server.return_value = True
    _set_global_settings(EventState.PRE_EVENT)

    with pytest.raises(ValueError):
        discord.DiscordMutation.resolve_invite_to_discord(None, GraphQLInfo(AnonymousUser()))
    assert not discord.invite_to_server.called


@pytest.mark.django_db
def test_inviting_to_discord_is_not_allowed_when_post_event(mocker):
    mocker.patch("virtualbarcamp.graphql.mutations.discord.invite_to_server")
    discord.invite_to_server.return_value = True
    _set_global_settings(EventState.POST_EVENT)

    with pytest.raises(ValueError):
        discord.DiscordMutation.resolve_invite_to_discord(None, GraphQLInfo(AnonymousUser()))
    assert not discord.invite_to_server.called
