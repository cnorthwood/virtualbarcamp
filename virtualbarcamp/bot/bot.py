import logging

import discord
from asgiref.sync import sync_to_async

from virtualbarcamp.discord import create_voice_channel, create_text_channel
from virtualbarcamp.home.models import GlobalSettings

LOGGER = logging.getLogger(__name__)


class BarCampBot(discord.Client):
    async def on_ready(self):
        LOGGER.info(f"Connected to Discord as {self.user}")

    async def on_message(self, message):
        if message.content.startswith("!breakout"):
            args = message.content.split(" ")
            if len(args) < 3:
                await message.channel.send(
                    "To create a breakout room, type `!breakout text/voice room name`, for example `!breakout voice Docker` for a breakout room to discuss Docker using voice"
                )
                return

            room_type = args[1].lower()
            name = " ".join(args[2:]).strip()
            breakout_category_id = await sync_to_async(
                lambda: GlobalSettings.objects.first().get_or_create_breakout_category_id()
            )()
            if room_type == "voice":
                channel_id = create_voice_channel(name, breakout_category_id)
                await message.channel.send(f"Created! You can now head over to <#{channel_id}>.")
            elif room_type == "text":
                channel_id = create_text_channel(name, breakout_category_id)
                await message.channel.send(f"Created! You can now head over to <#{channel_id}>.")
            else:
                await message.channel.send(
                    "I couldn't recognise that room type. To create a breakout room, type `!breakout text/voice room name`."
                )
