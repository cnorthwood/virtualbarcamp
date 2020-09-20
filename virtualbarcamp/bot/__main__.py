from django.conf import settings

from virtualbarcamp.bot.bot import BarCampBot

bot = BarCampBot()
bot.run(settings.DISCORD_BOT_TOKEN)
