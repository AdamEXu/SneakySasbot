import discord
from discord.ext import commands
import data_handler
import datetime
import random

help_output = """
## Sasbot Help
This is Adam The Great's interpretation of Sasbot. It contains an economy, and some fun commands.

**ECONOMY**
Make money using `|work`
Explore other jobs using `|job`
Buy useful items in the shop with `|shop`
Check how many coins you have with `|bal`
See your inventory with `|inv`
Use the bank using `|dep` and `|with`

**FUN**
View a random Sneaky Sasquatch meme with `|meme` ||If you would like to submit a meme, run `|submitmeme`.||

There will be more commands in future versions!
-# Version 0.1.0 (Test version)
"""

welcome_output = f"""
You seem to be new here! I have ignored your previous command and have setup your profile with default values and a coin balance of 0.

To start making coins, run `|work`.
Keep an eye on your hunger bar! If it hits 0, there will be consequences. To fill it, run `|eat [food]`, where food is the name of the food you want to eat.
To see what is in your inventory (and see what food you have to eat), run `|inv`.

Take a look at `|help` for more information.
"""

intents = discord.Intents.all()

client = commands.Bot(command_prefix='|', description="Test", intents=intents, help_command=None)

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.command()
async def work(ctx):
  user_id = ctx.author.id
  user_in_json = data_handler.ensure_user_in_json(user_id)
  if user_in_json:
    await ctx.reply(welcome_output)
  else:
    user_data = data_handler.get_user_data(user_id)
    user_job = user_data['work_job']
    last_work = user_data['last_work']
    job_data = data_handler.get_job_data(user_job)
    if last_work + job_data['cooldown'] > datetime.datetime.now().timestamp():
      seconds = datetime.timedelta(seconds=last_work + job_data['cooldown'] - datetime.datetime.now().timestamp()).seconds
      await ctx.reply(f"Please wait {seconds} seconds before working again.")
    else:
      earning_min = job_data['earning_min']
      earning_max = job_data['earning_max']
      earnings = random.randint(earning_min, earning_max)
      user_data['last_work'] = datetime.datetime.now().timestamp()
      user_data['coin_balance'] += earnings
      user_data['earnings'] += earnings
      data_handler.save_user_data(user_id, user_data)
      await ctx.reply(f"You have earned {earnings} coins.")

@client.command()
async def bal(ctx):
  user_id = ctx.author.id
  user_in_json = data_handler.ensure_user_in_json(user_id)
  if user_in_json:
    await ctx.reply(welcome_output)
  else:
    user_data = data_handler.get_user_data(user_id)
    balance = user_data['coin_balance']
    bank_balance = user_data['bank_balance']
    bank_lvl = user_data['bank_lvl']
    user_publicname = ctx.author.display_name
    if bank_lvl == 0:
      bank_info = f"""**Bank**
      You haven't unlocked the bank yet. See the `|shop` for more information."""
    else:
      bank_info = f"""**Bank**
      Bank Balance: {bank_balance}
      Bank Level: {bank_lvl}"""
    embed = discord.Embed(title=f"{user_publicname}'s Balance", description=f"""**Coin Balance**\n{balance}\n\n{bank_info}""", color=0x00ff00)
  await ctx.reply(embed=embed)

shop_items = [
  {"name": "Item 1", "description": "This is item 1.", "price": 100},
  {"name": "Item 2", "description": "This is item 2.", "price": 200},
  {"name": "Fox Mischief.", "description": "Very Mischief.", "price": 300},
]

# Function to create the embed for the shop
def create_shop_embed(index):
  item = shop_items[index]
  embed = discord.Embed(
    title=f"Shop - {item['name']}",
    description=item['description'],
    color=0x00ff00
  )
  embed.add_field(name="Price", value=f"{item['price']} coins")
  embed.set_footer(text=f"Page {index + 1} of {len(shop_items)}")
  return embed

@client.command()
async def shop(ctx):
  current_index = 0
  message = await ctx.send(embed=create_shop_embed(current_index))

  # Add reactions for navigation and buying
  await message.add_reaction('⬅️')
  await message.add_reaction('💰')
  await message.add_reaction('➡️')

  def check(reaction, user):
    return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['⬅️', '➡️', '💰']

  while True:
    try:
      reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

      if str(reaction.emoji) == '⬅️':
        current_index = (current_index - 1) % len(shop_items)
        await message.edit(embed=create_shop_embed(current_index))
        await message.remove_reaction(reaction, user)

      elif str(reaction.emoji) == '➡️':
        current_index = (current_index + 1) % len(shop_items)
        await message.edit(embed=create_shop_embed(current_index))
        await message.remove_reaction(reaction, user)

      elif str(reaction.emoji) == '💰':
        print("Trying to buy")
        item = shop_items[current_index]
        await message.remove_reaction(reaction, user)
        await ctx.send(f"You have purchased {item['name']} for {item['price']} coins!")

    except Exception as e:
      break

@client.command()
async def help(ctx):
  await ctx.send(help_output)

client.run('')
