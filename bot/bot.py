import discord
from discord.ext import commands

from config import settings

import os

bot = commands.Bot(command_prefix=settings['PREFIX'])
bot.remove_command('help')


@bot.event
async def on_ready():
    print(settings['BOT_NAME'] + ' is ready')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name='-help'))


@bot.command()
async def on(ctx, extension = None):
    if extension is None:
        await ctx.send('Выбырите блок, который вы хотите включить')
    else:
        bot.load_extension(f'cogs.{extension}')


@bot.command()
async def off(ctx, extension = None):
    if extension is None:
        await ctx.send('Выбырите блок, который вы хотите выключить')
    else:
        bot.unload_extension(f'cogs.{extension}')


for filename in os.listdir('C:/Users/Romidamaru/source/repos/Discord-Bot/bot/cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def help(ctx):
    embed_set = discord.Embed(title='Справочник', color=0xe0f323)
    embed_set.add_field(name = 'Экономика', value = '-balance, -award, -take, -add-shop, -remove-shop, -shop, -buy, -casino', inline = False)
    embed_set.add_field(name = 'Картинки', value = '-blur, -contour, -emboss, -smooth, -detail', inline = False)
    embed_set.add_field(name = 'Развлечения', value = '-монетка, -шар, -cookie, -roll', inline = False)

    await ctx.send(embed=embed_set)


bot.run(settings['TOKEN'])