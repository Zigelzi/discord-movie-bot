import os

from discord.ext import commands
from dotenv import load_dotenv
from movie_request import get_movie_name
from utilities import is_valid_url

load_dotenv('envs/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
print(TOKEN)
bot = commands.Bot(command_prefix='/')

@bot.command(name='add')
async def add_movie(ctx, url, service):
    if ctx.channel.name == 'bottihärö':
        if (not is_valid_url(url)):
            await ctx.channel.send(f'Currently only suggestions from Rotten Tomatoes (https://www.rottentomatoes.com/) are accepted. The URL you provided: {url}')
        movie_request = {
            'message_id': str(ctx.message.id),
            'name': '',
            'requester': ctx.message.author.name,
            'release_year': '',
            'service': service,
            'url': url,
            'votes': 0,
            'watched': False
        }
        print(f'User added movie with URL {url} in the channel {ctx.channel.name}')
        print(f'User added movie in service {service} in the channel {ctx.channel.name}')
        print(f'Message id: {ctx.message.id} by {ctx.message.author}')
        movie_request['name'] = get_movie_name(url)
        # add_movie_to_sheet(movie_request)
        await ctx.channel.send(f'Requested movie: {url} in service {service}')

@add_movie.error
async def add_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send(f'You seem to tried to request a movie without required argument. Error: {error}')

bot.run(TOKEN)

