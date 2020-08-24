"""
Created by Epic at 8/24/20
"""
from discord.ext import commands
from os import environ as env, remove
import typing
import discord
import aiohttp
from io import BytesIO
from stickify import stickify

bot = commands.Bot(command_prefix=commands.when_mentioned_or(env["PREFIX"]),
                   help_command=commands.MinimalHelpCommand(no_category="General"))
bot.load_extension("jishaku")


@bot.command()
async def stickbug(ctx: commands.Context, user: typing.Optional[discord.User]):
    message: discord.Message = ctx.message
    image_file = BytesIO()
    if len(message.attachments) == 1:
        attachment: discord.Attachment = message.attachments[0]
        await attachment.save(image_file)
    elif isinstance(user, discord.User):
        avatar_url = str(user.avatar_url)
        async with aiohttp.request("GET", avatar_url) as response:
            image_file.write(await response.read())
    else:
        return await ctx.send("Mention a user or attach a image or send a link to stickbugify them!")

    async with ctx.channel.typing():
        output = await stickify(image_file.read())

        await ctx.send(file=discord.File(output, filename="getsticked.mp4"))
        image_file.close()
        output.close()


bot.run(env["TOKEN"])
