import discord
from discord.ext import commands
import data_handler
import datetime
import random
from definitions import *
import os

intents = discord.Intents.all()

client = commands.Bot(command_prefix=['|', 'sneak ', 'Sneak ', 'SNEAK ', '<@1272666435063251057> ', '<@1272666435063251057>'], description="Test", intents=intents, help_command=None)

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
    user_vehicle = user_data['vehicle']
    vehicle_modifer = 1
    calc_cooldown = job_data['cooldown']
    if user_vehicle != '':
        vehicle_modifer = vehicle_modifers[user_vehicle]
        calc_cooldown = job_data['cooldown'] * vehicle_modifer
    boost_message = ""
    if vehicle_modifer < 1:
        rounded_modifer = round((1 - vehicle_modifer) * 100)
        boost_message = f"Your {id_to_name[user_vehicle]} is boosting your cooldown by {rounded_modifer}%!"
    if last_work + calc_cooldown > datetime.datetime.now().timestamp():
        seconds = round(last_work + calc_cooldown - datetime.datetime.now().timestamp())
        embed = discord.Embed(title="Work", description=f"You can work again in {seconds} seconds.\n{boost_message}", color=0xff0000)
        await ctx.reply(embed=embed)
    else:
        earning_min = job_data['earning_min']
        earning_max = job_data['earning_max']
        earnings = random.randint(earning_min, earning_max)
        user_data['last_work'] = datetime.datetime.now().timestamp()
        user_data['coin_balance'] += earnings
        user_data['earnings'] += earnings
        data_handler.save_user_data(user_id, user_data)
        random_work_messages = work_messages[user_data['work_job']]
        random_work_message = random.choice(random_work_messages)
        user_data['hunger'] -= 1
        work_message = f"{random_work_message}\n\nYour earnings: <:coin:1273754255433531565> **{earnings}**\nYou can work again in {calc_cooldown} seconds.\n{boost_message}\n\nYour hunger bar has decreased by 1 point. Current hunger: {user_data['hunger']} / {user_data['hunger_max']}."
        embed = discord.Embed(title="Work", description=work_message, color=0x00ff00)
        await ctx.reply(embed=embed)

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
  embed.add_field(name="Total Earnings (Lifetime)", value=user_data['earnings'])
  embed.add_field(name="Hunger Bar", value=f"{user_data['hunger']} / {user_data['hunger_max']}")
  await ctx.reply(embed=embed)

@client.command()
async def inv(ctx):
    user_id = ctx.author.id
    user_in_json = data_handler.ensure_user_in_json(user_id)
    if user_in_json:
        await ctx.reply(welcome_output)
    else:
        user_data = data_handler.get_user_data(user_id)
        inventory = user_data['inventory']
        inventory_list = ""
        for item in inventory:
            inventory_list += f"* {id_to_name[item]}\n"
        vehicle_list = ""
        for vehicle in user_data['vehicles']:
            vehicle_list += f"* {id_to_name[vehicle]}\n"
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Inventory", description=f"Hunger Bar: {user_data['hunger']} / {user_data['hunger_max']}", color=0x00ff00)
        embed.add_field(name="Food Items", value=inventory_list)
        embed.add_field(name="Vehicles", value=vehicle_list)
        embed.add_field(name="Current Vehicle", value=id_to_name[user_data['vehicle']])
        await ctx.reply(embed=embed)

def create_shop_embed(index, shop, shop_name):
    item = shop[index]
    embed = discord.Embed(
        title=f"{shop_name} - {item['name']}",
        description=item['description'],
        color=0x00ff00
    )
    embed.add_field(name="Price", value=f"{item['price']} coins")
    embed.set_footer(text=f"Page {index + 1} of {len(shop)}")
    return embed

@client.command()
async def shop(ctx, shop_name=None):
    if shop_name:
        if shop_name.lower() == "food" or shop_name.lower() == "foods":
            await display_food_shop(ctx)
        elif shop_name.lower() == "vehicle" or shop_name.lower() == "vehicles" or shop_name.lower() == "car" or shop_name.lower() == "cars":
            await display_vehicle_shop(ctx)
        elif shop_name.lower() == "special" or shop_name.lower() == "specials":
            await display_special_shop(ctx)
    embed = discord.Embed(
        title="Select a Shop",
        description="Please select a shop by clicking on one of the reactions below:\n\n"
                    "🍔 Food Shop\n"
                    "🚗 Vehicle Shop\n"
                    "✨ Special Shop",
        color=0x00ff00
    )
    embed.set_footer(text="Tip: Next time, you can use |shop [shop name] to directly access a shop. For example, |shop food to access the food shop.")

    message = await ctx.send(embed=embed)
    await message.add_reaction('🍔')
    await message.add_reaction('🚗')
    await message.add_reaction('✨')

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['🍔', '🚗', '✨']

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

        if str(reaction.emoji) == '🍔':
            await message.delete()
            await display_food_shop(ctx)

        elif str(reaction.emoji) == '🚗':
            await message.delete()
            await display_vehicle_shop(ctx)

        elif str(reaction.emoji) == '✨':
            await message.delete()
            await display_special_shop(ctx)

    except Exception as e:
        print(e)

async def display_food_shop(ctx):
    current_index = 0
    message = await ctx.send(embed=create_shop_embed(current_index, food_shop_items, "Food Shop"))

    await message.add_reaction('⬅️')
    await message.add_reaction('💰')
    await message.add_reaction('➡️')

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['⬅️', '➡️', '💰']

    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)

            if str(reaction.emoji) == '⬅️':
                current_index = (current_index - 1) % len(food_shop_items)
                await message.edit(embed=create_shop_embed(current_index, food_shop_items, "Food Shop"))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '➡️':
                current_index = (current_index + 1) % len(food_shop_items)
                await message.edit(embed=create_shop_embed(current_index, food_shop_items, "Food Shop"))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '💰':
                item = food_shop_items[current_index]
                await message.remove_reaction(reaction, user)
                user_data = data_handler.get_user_data(ctx.author.id)
                if user_data['coin_balance'] < item['price']:
                    await ctx.send("You do not have enough coins to purchase this item.")
                else:
                    user_data['coin_balance'] -= item['price']
                    user_data['inventory'].append(item['id'])
                    data_handler.save_user_data(ctx.author.id, user_data)
                    await ctx.send(f"You have purchased {item['name']} for {item['price']} coins!")
        except Exception as e:
            print(e)
            break

def create_vehicle_embed(user_id, index):
    item = vehicle_shop_items[index]
    user_info = data_handler.get_user_data(user_id)
    if item["id"] == user_info["vehicle"]:
        embed = discord.Embed(
            title=f"Vehicle Shop - {item['name']}",
            description=item['description'],
            color=0x00ff00
        )
        embed.add_field(name="Owned", value="Currently equipped as your active vehicle.")
        embed.set_footer(text=f"Page {index + 1} of {len(vehicle_shop_items)}")
        return embed
    elif item["id"] in user_info["vehicles"]:
        embed = discord.Embed(
            title=f"Vehicle Shop - {item['name']}",
            description=item['description'],
            color=0x00ff00
        )
        embed.add_field(name="Owned", value=f"Click 💰 to equip it as your current vehicle and gain its bonus.")
        embed.set_footer(text=f"Page {index + 1} of {len(vehicle_shop_items)}")
        return embed
    else:
        embed = discord.Embed(
            title=f"Vehicle Shop - {item['name']}",
            description=item['description'],
            color=0x00ff00
        )
        embed.add_field(name="Price", value=f"This vehicle costs {item['price']} coins")
        embed.set_footer(text=f"Page {index + 1} of {len(vehicle_shop_items)}")
        return embed

async def display_vehicle_shop(ctx):
    current_index = 0
    message = await ctx.send(embed=create_vehicle_embed(ctx.author.id, current_index))

    await message.add_reaction('⬅️')
    await message.add_reaction('💰')
    await message.add_reaction('➡️')

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['⬅️', '➡️', '💰']

    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == '⬅️':
                current_index = (current_index - 1) % len(vehicle_shop_items)
                await message.edit(embed=create_vehicle_embed(ctx.author.id, current_index))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '➡️':
                current_index = (current_index + 1) % len(vehicle_shop_items)
                await message.edit(embed=create_vehicle_embed(ctx.author.id, current_index))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '💰':
                item = vehicle_shop_items[current_index]
                await message.remove_reaction(reaction, user)
                user_data = data_handler.get_user_data(ctx.author.id)
                if user_data['coin_balance'] < item['price']:
                    await ctx.send("You do not have enough coins to purchase this vehicle.")
                elif item['id'] in user_data['vehicles']:
                    user_data['vehicle'] = item['id']
                    await ctx.send(f"Equipped {item['name']} as your active vehicle.")
                else:
                    user_data['coin_balance'] -= item['price']
                    user_data['vehicles'].append(item['id'])
                    user_data['vehicle'] = item['id']
                    data_handler.save_user_data(ctx.author.id, user_data)
                    await ctx.send(f"You have purchased {item['name']} for {item['price']} coins! It is now your active vehicle.\n-# To switch vehicles, use the shop and click buy on the vehicle (it won't charge you again if you already own it).")
                await message.edit(embed=create_vehicle_embed(ctx.author.id, current_index))
        except Exception as e:
            break

async def display_special_shop(ctx):
    await ctx.send("Special Shop coming soon!")
    return
    current_index = 0
    message = await ctx.send(embed=create_shop_embed(current_index, special_shop_items, "Special Shop"))

    await message.add_reaction('⬅️')
    await message.add_reaction('💰')
    await message.add_reaction('➡️')

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['⬅️', '➡️', '💰']

    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == '⬅️':
                current_index = (current_index - 1) % len(special_shop_items)
                await message.edit(embed=create_shop_embed(current_index, special_shop_items, "Special Shop"))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '➡️':
                current_index = (current_index + 1) % len(special_shop_items)
                await message.edit(embed=create_shop_embed(current_index, special_shop_items, "Special Shop"))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '💰':
                item = special_shop_items[current_index]
                await message.remove_reaction(reaction, user)
                user_data = data_handler.get_user_data(ctx.author.id)
                if item['upgradeable'] and item['id'] in user_data['upgrades']:
                    await ctx.send(f"You already own and upgraded {item['name']}.")
                elif user_data['coin_balance'] < item['price']:
                    await ctx.send("You do not have enough coins to purchase this item.")
                else:
                    user_data['coin_balance'] -= item['price']
                    if item['upgradeable']:
                        user_data['upgrades'].append(item['id'])
                    else:
                        user_data['inventory'].append(item['id'])
                    data_handler.save_user_data(ctx.author.id, user_data)
                    await ctx.send(f"You have purchased {item['name']} for {item['price']} coins!")
        except Exception as e:
            break

def create_job_embed(index):
    job = jobs_list[index]
    job_info = data_handler.get_job_data(job)
    embed = discord.Embed(
        title=f"Job - {job_info['name']}",
        description=job_info['description'],
        color=0x00ff00
    )
    embed.add_field(name="Earnings", value=f"{job_info['earning_min']} - {job_info['earning_max']} coins")
    embed.add_field(name="Cooldown", value=f"{job_info['cooldown']} seconds")
    embed.add_field(name="Cost to Apply", value=f"{job_info['cost']} coins")
    embed.set_footer(text=f"Page {index + 1} of {len(jobs_list)}")
    return embed

@client.command()
async def jobs(ctx):
    current_index = 0
    message = await ctx.send(embed=create_job_embed(current_index))

    await message.add_reaction('⬅️')
    await message.add_reaction('💼')
    await message.add_reaction('➡️')

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['⬅️', '➡️', '💼']

    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == '⬅️':
                await message.remove_reaction(reaction, user)
                current_index = (current_index - 1) % len(jobs_list)
                await message.edit(embed=create_job_embed(current_index))

            elif str(reaction.emoji) == '➡️':
                await message.remove_reaction(reaction, user)
                current_index = (current_index + 1) % len(jobs_list)
                await message.edit(embed=create_job_embed(current_index))

            elif str(reaction.emoji) == '💼':
                job = jobs_list[current_index]
                user_data = data_handler.get_user_data(ctx.author.id)
                job_data = data_handler.get_job_data(job)
                
                if user_data['coin_balance'] < job_data['cost']:
                    await ctx.send("You do not have enough coins to apply for this job.")
                else:
                    user_data['coin_balance'] -= job_data['cost']
                    user_data['work_job'] = job
                    user_data['last_work'] = 0
                    data_handler.save_user_data(ctx.author.id, user_data)
                    await ctx.send(f"You have applied for the job {job}! Your work cooldown has been reset. Use |work to start working.")

        except Exception as e:
            break

@client.command()
async def use(ctx, item_name):
    user_data = data_handler.get_user_data(ctx.author.id)
    inventory = user_data['inventory']
    if len(inventory) == 0:
        await ctx.send(f"You do not have any items in your inventory, therefore you cannot use {id_to_name[item_name]}.")
        return
    if item_name not in inventory:
        await ctx.send(f"You do not have {id_to_name[item_name]} in your inventory. Maybe you can buy it from the shop?")
        return
    # get item type
    item_type = item_type_from_id[item_name]
    if item_type == "food":
        refill = food_hunger_refill[item_name]
        user_data['hunger'] += refill
        if user_data['hunger'] > user_data['hunger_max']:
            user_data['hunger'] = user_data['hunger_max']
        inventory.remove(item_name, 1)
        ctx.send(f"You ate a {id_to_name[item_name]} and refilled your hunger by {refill} points. Your hunger bar is now at {user_data['hunger']} points.")
    else:
        ctx.send("That item is not usable or does not exist. Perhaps check your spelling?")

@client.command()
async def help(ctx):
  embed = discord.Embed(
    title="Sasbot Help",
    description=help_output,
  )
  await ctx.send(embed=embed)

client.run(os.getenv('TOKEN'))
