import logging

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
import requests
from social_django.utils import load_strategy

from virtualbarcamp.grid.models import Room, Slot

LOGGER = logging.getLogger(__name__)


class RefreshTokenMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            discord_user = request.user.social_auth.get(provider="discord")
            if discord_user.access_token_expired():
                try:
                    discord_user.refresh_token(load_strategy())
                except:
                    LOGGER.warning("Unable to refresh token", exc_info=True)
                    logout(request)

        return self._get_response(request)


def is_on_server(user: User):
    social_auth = user.social_auth.get(provider="discord")
    response = requests.get(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/members/{social_auth.uid}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
    )
    if response.status_code == 404:
        return False
    else:
        response.raise_for_status()
        discord_nick = response.json()["nick"]
        if discord_nick and discord_nick != user.username:
            user.username = discord_nick
            user.save()
        return True


def invite_to_server(user: User):
    social_auth = user.social_auth.get(provider="discord")
    response = requests.put(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/members/{social_auth.uid}",
        json={"access_token": social_auth.get_access_token(load_strategy())},
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
    )
    response.raise_for_status()
    return response.status_code == 201


def remove_from_server(user: User):
    social_auth = user.social_auth.get(provider="discord")
    response = requests.put(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/members/{social_auth.uid}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
    )
    response.raise_for_status()
    return response.status_code == 204


def create_category(name: str):
    response = requests.post(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/channels",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        json={"name": name, "type": 4},
    )
    response.raise_for_status()
    return response.json()["id"]


def create_text_channel(name: str, parent_id: str):
    response = requests.post(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/channels",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        json={"name": name, "type": 0, "parent_id": parent_id},
    )
    response.raise_for_status()
    return response.json()["id"]


def presenter_only_permissions(presenter_role_id: str):
    STREAM_PERMISSION = 0x00000200
    SPEAK_PERMISSION = 0x00200000
    CONNECT_PERMISSION = 0x00100000
    everyone_role_id = settings.DISCORD_GUILD_ID
    moderator_role_id = settings.DISCORD_MODERATOR_ROLE_ID

    return [
        {
            "id": everyone_role_id,
            "type": "role",
            "deny": CONNECT_PERMISSION | STREAM_PERMISSION | SPEAK_PERMISSION,
        },
        {
            "id": moderator_role_id,
            "type": "role",
            "allow": CONNECT_PERMISSION | STREAM_PERMISSION | SPEAK_PERMISSION,
        },
        {
            "id": presenter_role_id,
            "type": "role",
            "allow": CONNECT_PERMISSION | STREAM_PERMISSION | SPEAK_PERMISSION,
        },
    ]


def max_voice_bitrate():
    response = requests.get(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
    )
    response.raise_for_status()
    return [96e3, 128e3, 256e3, 384e3][response.json()["premium_tier"]]


def create_voice_channel(name: str, parent: str, presenter_role_id: (str, None) = None):
    response = requests.post(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/channels",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        json={
            "name": name,
            "type": 2,
            "parent_id": parent,
            "bitrate": max_voice_bitrate(),
            "permission_overwrites": []
            if presenter_role_id is None
            else presenter_only_permissions(presenter_role_id),
        },
    )
    response.raise_for_status()
    return response.json()["id"]


def update_channel_name(channel_id: str, name: str):
    response = requests.patch(
        f"https://discord.com/api/channels/{channel_id}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        json={"name": name},
    )
    response.raise_for_status()


def delete_channel(channel_id: str):
    response = requests.delete(
        f"https://discord.com/api/channels/{channel_id}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
    )
    response.raise_for_status()


def create_role(name: str):
    response = requests.post(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/roles",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        json={"name": name},
    )
    response.raise_for_status()
    return response.json()["id"]


def update_role_name(role_id: str, name: str):
    response = requests.patch(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/roles/{role_id}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        json={"name": name},
    )
    response.raise_for_status()
    return response.json()["id"]


def delete_role(role_id: str):
    response = requests.delete(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/roles/{role_id}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
    )
    response.raise_for_status()


def sync_channels(room: Room):
    if not room.discord_category_id:
        room.discord_category_id = create_category(room.room_name)
    else:
        update_channel_name(room.discord_category_id, room.room_name)

    if not room.discord_presenter_role_id:
        room.discord_presenter_role_id = create_role(f"{room.room_name} Presenter")
    else:
        update_role_name(room.discord_presenter_role_id, f"{room.room_name} Presenter")

    if not room.discord_presentation_channel_id:
        room.discord_presentation_channel_id = create_voice_channel(
            room.room_name, room.discord_category_id, room.discord_presenter_role_id
        )
    else:
        update_channel_name(room.discord_presentation_channel_id, room.room_name)

    if not room.discord_discussion_channel_id:
        room.discord_discussion_channel_id = create_text_channel(
            f"{room.room_name} Discussion", room.discord_category_id
        )
    else:
        update_channel_name(room.discord_discussion_channel_id, f"{room.room_name} Discussion")


def delete_channels(room: Room):
    if room.discord_presentation_channel_id:
        delete_channel(room.discord_presentation_channel_id)
    if room.discord_discussion_channel_id:
        delete_channel(room.discord_discussion_channel_id)
    if room.discord_category_id:
        delete_channel(room.discord_category_id)
    if room.discord_presenter_role_id:
        delete_role(room.discord_presenter_role_id)


def open_channel_to_all(channel_id: str):
    response = requests.patch(
        f"https://discord.com/api/channels/{channel_id}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        json={"permission_overwrites": []},
    )
    response.raise_for_status()


def limit_channel_to_presenters(channel_id: str, presenter_role_id: str):
    response = requests.patch(
        f"https://discord.com/api/channels/{channel_id}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        json={"permission_overwrites": presenter_only_permissions(presenter_role_id)},
    )
    response.raise_for_status()


def get_users_with_role(role_id: str):
    # TODO: handle more than 1000 members
    response = requests.get(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/members",
        params={"limit": 1000},
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
    )
    response.raise_for_status()
    for member in response.json():
        if role_id in member["roles"]:
            yield member["user"]["id"]


def add_role_to_user(role_id: str, user: User):
    user_id = user.social_auth.get(provider="discord").uid
    response = requests.put(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/members/{user_id}/roles/{role_id}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
    )
    response.raise_for_status()


def remove_role_from_user(role_id: str, user_id: str):
    response = requests.delete(
        f"https://discord.com/api/guilds/{settings.DISCORD_GUILD_ID}/members/{user_id}/roles/{role_id}",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
    )
    response.raise_for_status()


def send_message(channel_id: str, message: str):
    response = requests.post(
        f"https://discord.com/api/channels/{channel_id}/messages",
        headers={"authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        json={"content": message},
    )
    response.raise_for_status()


def start_slot(slot: Slot):
    try:
        if slot.talk.open_discussion:
            open_channel_to_all(slot.room.discord_presentation_channel_id)
        else:
            add_role_to_user(slot.room.discord_presenter_role_id, slot.talk.owner)
            for speaker in slot.talk.other_speakers.all():
                add_role_to_user(slot.room.discord_presenter_role_id, speaker)
        send_message(slot.room.discord_discussion_channel_id, f"Starting now! {slot.talk.title}")
    except Slot.talk.RelatedObjectDoesNotExist:
        pass


def end_slot(slot: Slot):
    for user_id in get_users_with_role(slot.room.discord_presenter_role_id):
        remove_role_from_user(slot.room.discord_presenter_role_id, user_id)
    limit_channel_to_presenters(
        slot.room.discord_presentation_channel_id, slot.room.discord_presenter_role_id
    )
    try:
        send_message(
            slot.room.discord_discussion_channel_id,
            f"Finishing: {slot.talk.title}\nCheck what's next at https://online.barcampmanchester.co.uk",
        )
    except Slot.talk.RelatedObjectDoesNotExist:
        pass
