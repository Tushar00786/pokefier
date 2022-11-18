import cv2
import time
import discord
import requests
import numpy as np
import tensorflow as tf

def catch(model: tf.keras.Sequential, pokemons: list, image_url: str, message: discord.Message, loop) -> None:
    name = identify(model, pokemons, image_url)
    catch_string = f"<@716390085896962058> c {name.lower()}"

    if loop.is_closed() == False:
        loop.create_task(message.channel.send(catch_string))

    return


def identify(model: tf.keras.Sequential, pokemons: list, pokemon_image: str) -> str:
    original_image = cv2.imdecode(np.asarray(bytearray(requests.get(
        pokemon_image, stream=True).raw.read()), dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    image = original_image

    # resize the image to match dimensions required by the model
    img = cv2.resize(image, (200, 125))

    img = img/255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    idx = np.argmax(pred, axis=1).tolist()[0]

    pred_name = pokemons[idx]

    return pred_name
