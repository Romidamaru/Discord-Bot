import discord
from discord.ext import commands

import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun cog is ready')


    @commands.command(aliases=['cookie', 'печенька'])
    async def __cookie(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send(embed=discord.Embed(description=f'Держи печеньку, {ctx.author.mention} :cookie:!'))
        else:
            await ctx.send(embed=discord.Embed(description=f'Держи печеньку, {member.mention} :cookie:!'))


    @commands.command(aliases=['шар'])
    async def __8ball(self, ctx, question=None):
        responses = ['Бесспорно',
                 'Предрешено',
                 'Никаких сомнений',
                 'Определённо да',
                 'Можешь быть уверен в этом',
                 'Мне кажется — «да»',
                 'Вероятнее всего',
                 'Хорошие перспективы',
                 'Знаки говорят — «да»',
                 'Да',
                 'Пока не ясно, попробуй снова',
                 'Спроси позже',
                 'Лучше не рассказывать',
                 'Сейчас нельзя предсказать',
                 'Сконцентрируйся и спроси опять',
                 'Даже не думай',
                 'Мой ответ — «нет»',
                 'По моим данным — «нет»',
                 'Перспективы не очень хорошие',
                 'Весьма сомнительно']
        if question is None:
            await ctx.send('Вам нужно что-нибудь спросить')
        else:
            await ctx.send(f'{question}? {random.choice(responses)}')


    @commands.command(aliases=['монетка'])
    async def heads_or_tails(self, ctx, choice_of_member=None):
        responses = ['орёл', 'решка']

        if choice_of_member is None:
            await ctx.send('Выберите орла или решку')
        else:
            await ctx.send(f'Говоришь {choice_of_member}? Результат - **{random.choice(responses)}**')

    @commands.command(aliases=['roll'])
    async def __roll(self, ctx):
        rand_roll = random.randint(1, 6)
        await ctx.send(f'Выпало {rand_roll} :game_die:')


def setup(bot):
	bot.add_cog(Fun(bot))