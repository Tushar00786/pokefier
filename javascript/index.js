const WHITELISTED_GUILDS = ['696969696969', '420420420420'] // replace with servers you want to auto-catch in
const TOKEN = "" // put your auth token inside the double quotes

const identifier = "" // repl link to pokefier api, contact me on discord to avail

const { Client } = require("discord.js-selfbot-v13");
const client = new Client({checkUpdate: false}); 

const axios = require('axios');

client.on("ready", async () => {
  console.log(`${client.user.username} is ready!`);
});

client.on("messageCreate", async message => {
    if (!message.guild) return;

    if (message.author.id === "716390085896962058") {
        if ((message.embeds.length > 0) && message.embeds[0].title.includes('wild pokémon has appeared!') && WHITELISTED_GUILDS.includes(message.guild.id)) {
            let pokemonImage = message.embeds[0].image.url;
            const pokedata = {'image_url': pokemonImage};
            
            await message.channel.sendTyping();
            let pokemon = await axios.post(identifier, pokedata);
            
            pokemon.name = pokemon.data;

            await message.channel.send(`<@716390085896962058> c ${pokemon.name.toLowerCase()}`);
        }
    };
});

client.login(TOKEN);
