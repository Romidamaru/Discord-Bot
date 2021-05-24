import discord
from discord.ext import commands

import sqlite3

import asyncio
import random

db = sqlite3.connect('economic.db')
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            id INT,
            cash BIGINT,
            lvl INT
        )""")
db.commit()

sh = sqlite3.connect('shop.db')
sh_curs = sh.cursor()

sh_curs.execute("""CREATE TABLE IF NOT EXISTS shop (
            role_id INT, 
            id INT,
            cost BIGINT
        )""")
sh.commit


class Economic(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print('Economic cog is ready')

	@commands.command(aliases=['balance'])
	async def __balance(self, ctx, member: discord.Member = None):
		if member is None:
			if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
				cursor.execute(f'INSERT INTO users VALUES ("{ctx.author}", {ctx.author.id}, 0, 0)')
				db.commit()
				await ctx.send(embed=discord.Embed(color=0x2bdea5, description=f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]}** :herb:"""))
			else:
				await ctx.send(embed=discord.Embed(color=0x2bdea5, description=f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]}** :herb:"""))

		else:
			if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
				cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0)')
				db.commit()
				await ctx.send(embed=discord.Embed(color=0x2bdea5, description=f"""Баланс пользователя **{member}** составляет **{cursor.execute('SELECT cash FROM users WHERE id = {}'.format(member.id)).fetchone()[0]}** :herb:"""))
			else:
				await ctx.send(embed=discord.Embed(color=0x2bdea5, description=f"""Баланс пользователя **{member}** составляет **{cursor.execute('SELECT cash FROM users WHERE id = {}'.format(member.id)).fetchone()[0]}** :herb:"""))

	@commands.command(aliases=['award'])
	@commands.cooldown(1, 21600, commands.BucketType.user)
	async def __award(self, ctx, amount: int=100):
		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
	 		cursor.execute(f'INSERT INTO users VALUES ("{ctx.author}", {ctx.author.id}, 0, 0)')

	 		cursor.execute('UPDATE users SET cash = cash + {} WHERE id = {}'.format(amount, ctx.author.id))
	 		db.commit()
	 		await ctx.send(embed=discord.Embed(color=0x2bdea5, description=f"""**{ctx.author}** получил **{amount}** :herb:. Теперь у тебя **{cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]}** :herb:"""))

		else:	
			cursor.execute('UPDATE users SET cash = cash + {} WHERE id = {}'.format(amount, ctx.author.id))
			db.commit()
			await ctx.send(embed=discord.Embed(color=0x2bdea5, description=f"""**{ctx.author}** получил **{amount}** :herb:. Теперь у тебя **{cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]}** :herb:"""))

	@commands.command(aliases=['give'])
	@commands.has_permissions(administrator=True)
	async def __give(self, ctx, member: discord.Member=None, amount: int=None):
		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
	 		cursor.execute(f'INSERT INTO users VALUES ("{ctx.author}", {ctx.author.id}, 0, 0)')
	 		db.commit()
	 		if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
	 			cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0)')
	 			db.commit()

		elif cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
	 		cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0)')
	 		db.commit()
	 		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
	 			cursor.execute(f'INSERT INTO users VALUES ("{ctx.author}", {ctx.author.id}, 0, 0)')
	 			db.commit()
		else:
	 		pass

		if member is None:
			await ctx.send('Выберие участника, которому хотите начислить :herb:')
		else:
			if amount is None:
				await ctx.send('Выберите кол-во :herb:, которое вы хотите начислить')
			elif amount <= 0:
				await ctx.send('Введите число не меньше и не равное нулю')
			else:
				cursor.execute('UPDATE users SET cash = cash + {} WHERE id = {}'.format(amount, member.id))
				db.commit()
				await ctx.send(embed=discord.Embed(color=0x2bdea5, description=f'**{member}** начислено **{amount}** :herb:'))

	@commands.command(aliases=['transfer'])
	async def __transfer(self, ctx, member: discord.Member=None, amount:int=None):
		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
	 		cursor.execute(f'INSERT INTO users VALUES ("{ctx.author}", {ctx.author.id}, 0, 0)')
	 		db.commit()
	 		if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
	 			cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0)')
	 			db.commit()

		elif cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
	 		cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0)')
	 		db.commit()
	 		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
	 			cursor.execute(f'INSERT INTO users VALUES ("{ctx.author}", {ctx.author.id}, 0, 0)')
	 			db.commit()
		else:
	 		pass

		if member is None:
			await ctx.send('Выберие участника, которому хотите передать :herb:')
		else:
			if amount is None:
				await ctx.send('Выберите кол-во :herb:, которое вы хотите передать')
			elif amount <= 0:
				await ctx.send('Введите число больше нуля')
			elif cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0] < amount:
				await ctx.send('У вас недостаточно :herb: для этого')
			else:
				cursor.execute('UPDATE users SET cash = cash - {} WHERE id = {}'.format(amount, ctx.author.id))
				cursor.execute('UPDATE users SET cash = cash + {} WHERE id = {}'.format(amount, member.id))
				db.commit()
				await ctx.send(embed=discord.Embed(color=0x2bdea5, description=f'**{ctx.author}** передал **{member}** **{amount}** :herb:')) 	

	@commands.command(aliases=['take'])
	@commands.has_permissions(administrator=True)
	async def __take(self, ctx, member:discord.Member=None, amount=None):
		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
	 		cursor.execute(f'INSERT INTO users VALUES ("{ctx.author}", {ctx.author.id}, 0, 0)')
	 		db.commit()
	 		if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
	 			cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0)')
	 			db.commit()

		elif cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
	 		cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0)')
	 		db.commit()
	 		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
	 			cursor.execute(f'INSERT INTO users VALUES ("{ctx.author}", {ctx.author.id}, 0, 0)')
	 			db.commit()
		else:
	 		pass

		if member is None:
	 		await ctx.send('Укажите пользователя, у которого хотите забрать :herb:')
		else:
	 		if amount is None:
	 			await ctx.send('Введите сумму, которую хотите забрать')
	 			cursor.execute('UPDATE users SET cash = cash - {} WHERE id = {}'.format(amount, member.id))
	 			db.commit()
	 			await ctx.send(embed=discord.Embed(color=0x2bdea5, description=f"""**{ctx.author}** забрал у **{member}** **{amount}** :herb:."""))

	@commands.command(aliases=['add-shop'])
	@commands.has_permissions(administrator=True)
	async def __add_shop(self, ctx, role: discord.Role=None, cost: int=None):
		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
			cursor.execute(f'INSERT INTO users VALUES IF NOT EXISTS ("{ctx.author}", {ctx.author.id}, 0, 0)')

		if role is None:
			await ctx.send('Пожалуйста, выберите роль, которую вы хотите добавить в магазин')
		else:
			if cost is None:
				await ctx.send('Пожалуйста, выберите цену для роли')
			elif cost < 0:
				await ctx.send('Цена не может быть меньше нуля')
			else:
				sh_curs.execute('INSERT INTO shop VALUES ({}, {}, {})'.format(int(role.id), ctx.guild.id, cost))
				sh.commit()
				await ctx.send(embed=discord.Embed(color=0x15d154, description='В магазин добавлена роль :white_check_mark:'))

	@commands.command(aliases=['remove-shop'])
	@commands.has_permissions(administrator=True)
	async def __remove_shop(self, ctx, role: discord.Role=None):
		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
			cursor.execute(f'INSERT INTO users VALUES IF NOT EXISTS ("{ctx.author}", {ctx.author.id}, 0, 0)')

		if role is None:
			await ctx.send('Пожалуйста, выберите роль, которую вы хотите удалить из магазина')
		else:
			sh_curs.execute('DELETE FROM shop WHERE role_id = {}'.format(role.id))
			sh.commit()
			await ctx.send(embed=discord.Embed(color=0xff0004, description='В магазине удалена роль :no_entry_sign:'))

	@commands.command(aliases=['shop'])
	async def __shop(self, ctx):
		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
			cursor.execute(f'INSERT INTO users VALUES IF NOT EXISTS ("{ctx.author}", {ctx.author.id}, 0, 0)')

		embed = discord.Embed(title='Магазин ролей', color=0xde2b92)

		for row in sh_curs.execute('SELECT role_id, cost FROM shop WHERE id = {}'.format(ctx.guild.id)):
			embed.add_field(
					name = f'Стоимость **{row[1]}** :herb:',
					value = f'Вы получите {ctx.guild.get_role(row[0]).mention}',
					inline = False
					)

		embed.set_image(url='https://i.redd.it/vqhezs2arkt21.png')

		await ctx.send(embed=embed)

	@commands.command(aliases=['buy', 'buy-role'])
	async def __buy(self, ctx, role: discord.Role=None):
		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
			cursor.execute(f'INSERT INTO users VALUES IF NOT EXISTS ("{ctx.author}", {ctx.author.id}, 0, 0)')

		if role is None:
			await ctx.send('Выберите роль, которую вы хотите купить')
		else:
			if role in ctx.author.roles:
				await ctx.send('У вас уже есть эта роль')
			elif sh_curs.execute('SELECT cost FROM shop WHERE role_id = {}'.format(role.id)).fetchone()[0] > cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]:
				await ctx.send('У вас недостаточно :herb: для покупки роли')
			else:
				await ctx.author.add_roles(role)
				cursor.execute('UPDATE users SET cash = cash - {0} WHERE id = {1}'.format(sh_curs.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
				await ctx.send('Ваши роли обновлены :crayon:')

	@commands.command(aliases=['casino'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def __casino(self, ctx, amount: int = None):
		if cursor.execute(f'SELECT id FROM users WHERE id = {ctx.author.id}').fetchone() is None:
			cursor.execute(f'INSERT INTO users VALUES IF NOT EXISTS ("{ctx.author}", {ctx.author.id}, 0, 0)')

		if amount is None:
			await ctx.send('Введите сумму, которую вы хотите поставить')
		else:
			if cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0] < amount:
				await ctx.send('У вас недостаточно :herb:')
			elif amount <= 0:
				await ctx.send('Введите сумму больше нуля')
			else:
				cursor.execute('UPDATE users SET cash = cash - {} WHERE id = {}'.format(amount, ctx.author.id))
				db.commit()
				rand = random.randint(0, 100)
				if rand > 60:
					sec_rand = random.randint(0, 100)
					if sec_rand >= 90:
						cursor.execute('UPDATE users SET cash = cash + {} WHERE id = {}'.format(amount*3, ctx.author.id))
						db.commit()
						await ctx.send(f'Ты выиграл {amount*3} :herb:')
					elif sec_rand > 50 and sec_rand < 90:
						cursor.execute('UPDATE users SET cash = cash + {} WHERE id = {}'.format(amount*2, ctx.author.id))
						db.commit()
						await ctx.send(f'Ты выиграл {amount*2} :herb:')
					elif sec_rand <= 50:
						cursor.execute('UPDATE users SET cash = cash + {} WHERE id = {}'.format(amount*1.5, ctx.author.id))
						db.commit()
						await ctx.send(f'Ты выиграл {amount*1.5} :herb:')
					else:
						pass
				else:
					cursor.execute('UPDATE users SET cash = cash + {} WHERE id = 760417364583251998'.format(amount))
					await ctx.send(f'Ты проиграл {amount} :herb:')

def setup(bot):
	bot.add_cog(Economic(bot))