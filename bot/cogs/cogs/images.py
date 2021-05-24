import discord
from discord.ext import commands
import os
import requests
from PIL import Image, ImageFilter
from io import BytesIO

class Images(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f'Images cog is ready')

	@commands.command()
	async def blur(self, ctx, url: str = None):
		if url is None:
			await ctx.send('Вставьте ссылку на картинку')
		else:
			response = requests.get(url)
			img = Image.open(BytesIO(response.content), mode='r')
			im = img.filter(ImageFilter.BLUR)
			b = BytesIO()
			im.save(b, format='PNG')
			byte_im = b.getvalue()
			with open('blur.png', 'wb') as img:
				img.write(byte_im)
				await ctx.send(file=discord.File("blur.png"))
			os.remove("blur.png")

	@commands.command()
	async def contour(self, ctx, url: str = None):
		if url is None:
			await ctx.send('Вставьте ссылку на картинку')
		else:
			response = requests.get(url)
			img = Image.open(BytesIO(response.content), mode='r')
			im = img.filter(ImageFilter.CONTOUR)
			b = BytesIO()
			im.save(b, format='PNG')
			byte_im = b.getvalue()
			with open('contour.png', 'wb') as img:
				img.write(byte_im)
				await ctx.send(file=discord.File("contour.png"))
			os.remove("contour.png")

	@commands.command()
	async def detail(self, ctx, url: str = None):
		if url is None:
			await ctx.send('Вставьте ссылку на картинку')
		else:
			response = requests.get(url)
			img = Image.open(BytesIO(response.content), mode='r')
			im = img.filter(ImageFilter.DETAIL)
			b = BytesIO()
			im.save(b, format='PNG')
			byte_im = b.getvalue()
			with open('detail.png', 'wb') as img:
				img.write(byte_im)
				await ctx.send(file=discord.File("detail.png"))
			os.remove("detail.png")

	@commands.command()
	async def smooth(self, ctx, url: str = None):
		if url is None:
			await ctx.send('Вставьте ссылку на картинку')
		else:
			response = requests.get(url)
			img = Image.open(BytesIO(response.content), mode='r')
			im = img.filter(ImageFilter.SMOOTH)
			b = BytesIO()
			im.save(b, format='PNG')
			byte_im = b.getvalue()
			with open('smooth.png', 'wb') as img:
				img.write(byte_im)
				await ctx.send(file=discord.File("smooth.png"))
			os.remove("smooth.png")

	@commands.command()
	async def emboss(self, ctx, url: str = None):
		if url is None:
			await ctx.send('Вставьте ссылку на картинку')
		else:
			response = requests.get(url)
			img = Image.open(BytesIO(response.content), mode='r')
			im = img.filter(ImageFilter.EMBOSS)
			b = BytesIO()
			im.save(b, format='PNG')
			byte_im = b.getvalue()
			with open('emboss.png', 'wb') as img:
				img.write(byte_im)
				await ctx.send(file=discord.File("emboss.png"))
			os.remove("emboss.png")

def setup(bot):
	bot.add_cog(Images(bot))