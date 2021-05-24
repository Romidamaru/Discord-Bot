import discord
from discord.ext import commands


class Errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print('Errors cog is ready')

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			embed = discord.Embed(title = "**Cooldown!**", description = f"Попробуйте снова через {round(error.retry_after/60)} минут", color = 0xff0004)
			await ctx.send(embed=embed)
			return
		elif isinstance(error, commands.MissingPermissions):
			embed = discord.Embed(title='Недостаточно прав')
			await ctx.send(embed=embed)
		elif isinstance(error, commands.CommandNotFound):
			embed = discord.Embed(title='Нет такой команды')
			await ctx.send(embed=embed)
		raise error


def setup(bot):
	bot.add_cog(Errors(bot))