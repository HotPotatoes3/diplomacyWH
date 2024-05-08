import os
import random
import shutil
import uuid
import PIL.Image
import discord
from discord.ext import commands, tasks
import requests
import responses
import sqlite3




def run_discord_bot(discord):
    TOKEN = os.environ['TOKEN']

    app_commands = discord.app_commands
    bot = commands.Bot(command_prefix="!!", intents=discord.Intents.all())
    bot.remove_command("help")

    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready!!")
        try:
            synced = await bot.tree.sync()
        except Exception as e:
            print(e)


    @bot.command()
    async def diplomacy(ctx):

        webhookList = await ctx.channel.webhooks()
        for i in webhookList:
            if i.name == "DiplomacyHook":
                await ctx.reply("Webhook already created, use this link when creating a game: " + i.url)
                return


        webhook = await ctx.channel.create_webhook(name="DiplomacyHook")
        await ctx.reply("Webhook has been created for this discord channel. When creating the game, paste this url for the webhook url: " + webhook.url)

    bot.run(TOKEN)
