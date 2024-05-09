import os
from discord import Colour
from discord.ext import commands, tasks
import re




def run_discord_bot(discord):
    TOKEN = os.environ['TOKEN']

    app_commands = discord.app_commands
    bot = commands.Bot(command_prefix=".!!", intents=discord.Intents.all())
    bot.remove_command("help")

    def extract_text_from_embed_field(embed_field_value):
        # Regular expression to capture text inside brackets
        text_pattern = re.compile(r'\[(.*?)]\(.*?\)')

        # Find the text inside the brackets
        match = text_pattern.search(embed_field_value)

        if match:
            return match.group(1)
        else:
            return None


    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready!!")
        try:
            synced = await bot.tree.sync()
        except Exception as e:
            print(e)

    @bot.event
    async def on_message(message):
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)



        if message.author == str(bot.user):
            print("Bot response")
        elif message.author.id == 1237832585728757935:
            print("Backstabbr response")
            if 'has created a new game on Backstabbr. You should join!' in user_message:
                await gameStart(message)
            elif 'Your game has adjudicated.' in user_message:
                await adjudicate(message)
            elif 'Your game on Backstabbr has begun!' in user_message:
                await start(message)
            elif 'Your game has ended.' in user_message:
                await endGame(message)

        else:
            print(f"{username} said: '{user_message}' ({channel})")

        await bot.process_commands(message)

    @bot.event
    async def on_reaction_add(reaction, user):
        message = reaction.message
        role = None

        if user != bot.user:
            print("Test1")
            if reaction.emoji == '✅' and reaction.message.author == bot.user:

                print("Test2")

                for i in message.guild.roles:
                    if '(BackStabbr)' in i.name and f"'{i.name[:len(i.name)-13]}'" in message.content:
                        print("Test3")
                        role = i
                        break


                try:
                    await user.add_roles(role)
                    print(f"Gave {user} the role: {role.name}")
                except Exception as e:
                    print(e)
                    return


    @bot.event
    async def on_reaction_remove(reaction, user):
        message = reaction.message
        role = None

        if user != bot.user:
            if reaction.emoji == '✅' and reaction.message.author == bot.user:

                for i in message.guild.roles:
                    if '(BackStabbr)' in i.name and f"'{i.name[:len(i.name)-13]}'" in message.content:
                        role = i

                try:
                    await user.remove_roles(role)
                    print(f"Removed {user}'s role: {role.name}")
                except Exception:
                    return

    async def endGame(message):
        content = message.content
        embed = message.embeds[0]
        role = ''
        for j in message.guild.roles:
            for field in embed.fields:
                if field.name == 'Game':
                    if j.name == extract_text_from_embed_field(str(field.value)) + ' (BackStabbr)':
                        role = j
        await message.channel.send(
            f"{role.mention}, the game has ended.")
        await role.delete()

    async def adjudicate(message):
        content = message.content
        embed = message.embeds[0]

        role = ''
        for j in message.guild.roles:
            for field in embed.fields:
                if field.name == 'Game':
                    if j.name == extract_text_from_embed_field(str(field.value)) + ' (BackStabbr)':
                        role = j

        await message.channel.send(f"{role.mention}, your game has been adjudicated. Refresh your game page and put in your next orders as soon as possible.")


    async def start(message):
        content = message.content
        embed = message.embeds[0]

        role = ''
        for j in message.guild.roles:
            for field in embed.fields:
                if field.name == 'Game':
                    if j.name == extract_text_from_embed_field(str(field.value)) + ' (BackStabbr)':
                        role = j

        await message.channel.send(f"{role.mention}, your game has been started. Refresh your game page and put in your next orders as soon as possible.")


    async def gameStart(message):
        content = message.content
        embed = message.embeds[0]

        role_name = ''

        for field in embed.fields:
            if field.name == 'Game':
                role_name = extract_text_from_embed_field(str(field.value)) + ' (BackStabbr)'
                role = await message.guild.create_role(name=role_name,colour=Colour.orange(),mentionable = True)
                break


        message2 = await message.channel.send(
            f"@everyone A BackStabbr game, '{role_name[:len(role_name)-13]}' has been created, click the link in the embed above to join the game. If you would like to participate and get pinged for whenever an adjudication occurs, react to this message with a ✅")

        await message2.add_reaction('✅')

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
