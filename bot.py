import os
import requests

from discord.ext import commands
from dotenv import load_dotenv
from movie_request import get_movie_name
from utilities import is_valid_url

load_dotenv("envs/.env")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="/")

api_root_url = "http://api:5000"

@bot.command(name="add")
async def add_movie(ctx, url, service):
    if ctx.channel.name == "bottihärö":
        if (not is_valid_url(url)):
            await ctx.channel.send(f"Currently only suggestions from Rotten Tomatoes (https://www.rottentomatoes.com/) are accepted. The URL you provided: {url}")
        movie_request = {
            "message_id": str(ctx.message.id),
            "name": "",
            "service": service,
            "suggested_by": ctx.message.author.name,            
            "url": url
        }

        # TODO: Remove these testing logs when ready
        print(f"User added movie with URL {url} in the channel {ctx.channel.name}")
        print(f"User added movie in service {service} in the channel {ctx.channel.name}")
        print(f"Message id: {ctx.message.id} by {ctx.message.author}")
        movie_request["name"] = get_movie_name(url)
        r = requests.post(f"{api_root_url}/movie_suggestions", json=movie_request)
        await ctx.channel.send(f"Added movie {movie_request['name']} from service {movie_request['service']} successfully with message ID {movie_request['message_id']}!")

@bot.listen()
async def on_raw_reaction_add(reaction):
    print(reaction)
    reply_channel = bot.get_channel(reaction.channel_id)
    message = await reply_channel.fetch_message(reaction.message_id)

    print(f"Message: {message}")
    print(f"Reactions:")
    for message_reaction in message.reactions:
        print(f"Number of :{message_reaction.emoji} - {message_reaction.count}")

    if reaction.emoji.name == "👍":
        # Check if movie exists for that message ID
        r = requests.get(f"{api_root_url}/movie_suggestions/{reaction.message_id}")

        if r.status_code == 404:
            await reply_channel.send(f"Movie with message ID {reaction.message_id} couldn't be found!")
        if r.status_code == 200:
            movie_suggestion = r.json()["data"]
            await reply_channel.send(f"{reaction.member.name} voted for movie: {movie_suggestion['name']} which has currently {movie_suggestion['votes']} votes")
    if reaction.emoji.name == "✅":
        # If it does, update the total number of votes
        # If it doesn"t, reply that movie with that message ID couldn"t be found
        
        # Check if movie exists for that message ID
        # Check if this is the first checkmark and if it is, mark the movie as watched
        await reply_channel.send(f"{reaction.member.name} marked the message ID: {reaction.message_id} as watched")
    
    await reply_channel.send(f"{reaction.member.name} reacted to message ID: {reaction.message_id} with reaction: {reaction.emoji.name}")
    


@add_movie.error
async def add_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send(f"You seem to tried to request a movie without required argument. Error: {error}")

bot.run(TOKEN)

