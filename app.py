import asyncio
import os
import random
from typing import Any

import discord
from discord.ext import commands

from src.healthcheck import Healthcheck

DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


async def get_partitions(items: list[Any], n: int) -> list[list[Any]]:
    random.shuffle(items)
    return [items[i::n] for i in range(n)]


@bot.event
async def setup_hook() -> None:
    healthcheck = Healthcheck(client=bot, port=8080)
    await healthcheck.start_server()


@bot.event
async def on_ready():
    await bot.tree.sync()


@bot.hybrid_command(name="breakouts")
async def breakouts(
    ctx: commands.context.Context,
    duration: int = 60,
    groups: int = 2,
) -> None:
    main_channel: discord.VoiceChannel = ctx.author.voice.channel

    guild: discord.Guild = ctx.guild
    channels: list[discord.VoiceChannel] = []
    for i in range(groups):
        channel = await guild.create_voice_channel(
            name=f"Breakout Room {i + 1}",
            category=main_channel.category,
        )
        channels.append(channel)

    members: list[discord.Member] = [
        member
        for member in main_channel.members
        if member.name not in ("svetlana.teacher.dc_10765",)
    ]
    member_groups: list[list[discord.Member]] = await get_partitions(
        items=members, n=groups
    )
    for i, member_group in enumerate(member_groups):
        for member in member_group:
            await member.move_to(channel=channels[i])

    await ctx.reply(
        content=f"Created {len(channels)} breakout rooms for {duration} seconds."
    )

    message: discord.Message = await ctx.send(
        f"Breakout rooms will close in {duration} seconds..."
    )
    while duration > 0:
        await asyncio.sleep(1)
        duration -= 1
        await message.edit(
            content=f"Breakout rooms will close in {duration} seconds..."
        )
    await message.delete()

    await ctx.send(
        content=f"Moving everyone back to {main_channel.name} channel.",
        delete_after=10,
    )

    for member in members:
        await member.move_to(channel=main_channel)

    for channel in channels:
        await channel.delete()


if __name__ == "__main__":
    bot.run(token=DISCORD_TOKEN)
