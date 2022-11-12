# library imports
import discord
import threading
import asyncio

# module imports
from src.utils import *
from src.helpers import solve

# load the model and initialize labels
model = tf.keras.models.load_model("model_pokemon.h5")

pokemons = # for self-use of labels, contact me on discord

# kickstart the model to reduce prediction time
identify(model, pokemons,
         "https://media.discordapp.net/attachments/1037799258637750363/1037814779005382716/pokemon.jpg")

# client vars
GUILD_ID = 6969696969 # replace with id of your server
TOKEN = "" # put your token inside the quotation marks

class Pokefier(discord.Client):
    async def on_ready(self):
        await self.change_presence(status=discord.Status.dnd)
        print('[READY] Logged in as', self.user)

    async def on_message(self, message):
        if message.author.id == 716390085896962058:
            if len(message.embeds) > 0 and "wild pokémon has appeared!" in message.embeds[0].title:
                if message.guild.id == GUILD_ID:
                    pokemon_image = message.embeds[0].image.url

                    await message.channel.trigger_typing()

                    threading.Thread(target=catch, args=(
                        self, model, pokemons, pokemon_image, message, asyncio.get_event_loop())).start()

                    await asyncio.sleep(5)

            if message.content.startswith("Whoa there") and str(self.user.id) in message.content:
                # getting the url from captcha message
                url = message.content.split(
                    "Whoa there. Please tell us you're human! ")[1]

                print("Got CAPTCHA! Attempting to solve.")

                self.captcha_url = url
                await self.close()


while True:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        client = Pokefier(
            guild_subscription_options=discord.GuildSubscriptionOptions.off())
        loop.run_until_complete(client.start(TOKEN))

    except:
        pass

    finally:
        loop.close()
        asyncio.set_event_loop(None)

        # client has logged out
        if hasattr(client, 'captcha_url'):
            solve(client.captcha_url)

            print("Successfully solved the CAPTCHA!")
