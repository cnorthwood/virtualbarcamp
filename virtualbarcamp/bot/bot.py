import logging

import discord
from asgiref.sync import sync_to_async
from discord import AllowedMentions

from django.conf import settings
from virtualbarcamp.discord import create_voice_channel, create_text_channel
from virtualbarcamp.grid.models import Room
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
        elif message.content.startswith("Finishing:") and message.author == self.user:
            room = await sync_to_async(
                lambda: Room.objects.filter(
                    discord_discussion_channel_id=message.channel.id
                ).first()
            )()
            if room:
                for channel in self.voice_channels:
                    if channel.id == room.discord_presentation_channel_id:
                        for member in channel.members:
                            await member.move_to(None)

    async def on_member_join(self, member):
        if settings.DISCORD_WELCOME_CHANNEL_ID:
            self.get_channel(settings.DISCORD_WELCOME_CHANNEL_ID).send(
                f"Welcome <@{member.id}>!",
                allowed_mentions=AllowedMentions(users=[member.id]),
            )

    async def on_voice_state_update(self, member, before, after):
        if before.channel is not None:
            breakout_category_id = await sync_to_async(
                lambda: GlobalSettings.objects.first().get_or_create_breakout_category_id()
            )()
            if (
                before.channel.category_id == breakout_category_id
                and len(before.channel.members) == 0
            ):
                await before.channel.delete(reason="Empty breakout room")
