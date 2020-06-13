import logging

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
import requests
from social_django.utils import load_strategy

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
