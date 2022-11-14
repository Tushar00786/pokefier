# put your token inside quotes
TOKEN = ""

# replace with server id's you want to autocatch on
WHITELISTED_SERVERS = [69696969696, 420420420420]

# library imports
import discord
import threading
import asyncio

# module imports
from src.utils import *
from src.helpers import solve

# load the model and initialize labels
model = tf.keras.models.load_model("model_pokemon.h5")

# contact me to get the values
pokemons = []

# kickstart the model to reduce prediction time
identify(model, pokemons,
         "https://media.discordapp.net/attachments/1037799258637750363/1037814779005382716/pokemon.jpg")


class Pokefier(discord.Client):
    async def on_ready(self):
        self.verifying = False
        await self.change_presence(status=discord.Status.dnd)
        print('[READY] Logged in as', self.user)

    async def on_message(self, message):
        if not hasattr(self, 'verifying'):
            self.verifying = False

        # only acknowledge the bot's messages if captcha is not being solved
        if message.author.id == 716390085896962058 and self.verifying == False:
            if len(message.embeds) > 0 and "wild pokémon has appeared!" in message.embeds[0].title:
                if message.guild.id in WHITELISTED_SERVERS:
                    pokemon_image = message.embeds[0].image.url

                    await message.channel.trigger_typing()

                    threading.Thread(target=catch, args=(
                        self, model, pokemons, pokemon_image, message, asyncio.get_event_loop())).start()

            if message.content.startswith("Whoa there") and str(self.user.id) in message.content:
                self.verifying = True

                # getting the url from captcha message
                url = message.content.split(
                    "Whoa there. Please tell us you're human! ")[1]

                print("Got CAPTCHA! Attempting to solve.")

                self.captcha_url = url

                threading.Thread(target=solve, args=(
                    client, self.captcha_url)).start()


client = Pokefier(
    guild_subscription_options=discord.GuildSubscriptionOptions.off())
client.run(TOKEN)
