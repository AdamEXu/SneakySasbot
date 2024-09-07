import asyncio
import discord
from discord.ext import commands, tasks
import data_handler
import datetime
import pytz
import random
import time
from definitions import *
import os
import base64
from cryptography.fernet import Fernet
import ast

intents = discord.Intents.all()

client = commands.Bot(command_prefix=['|', 'sneak ', 'Sneak ', 'SNEAK ', '<@1272666435063251057> ', '<@1272666435063251057>', 'ss ', 'Ss ', 'SS '], description="Test", intents=intents, help_command=None)

def zero_hunger_message(user_id):
    user_data = data_handler.get_user_data(user_id)
    user_data['hunger'] = 2
    user_data['coin_balance'] = user_data['coin_balance'] // 2
    data_handler.save_user_data(user_id, user_data)
    return "You fainted due to lack of food. The raccoon found you and took half of your coins. The raccoon also gave you some cookies to eat. Your hunger bar is now at 2 points."

@client.command()
async def work(ctx):
  user_id = ctx.author.id
  user_in_json = data_handler.ensure_user_in_json(user_id)
  if user_in_json == "added":
    await ctx.reply(welcome_output)
  else:
    user_data = data_handler.get_user_data(user_id)
    if 'mask_user' in user_data:
        user_id = user_data['mask_user']
        user_data = data_handler.get_user_data(user_id)
        user = await client.fetch_user(user_id)
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
    # time_stamp = f"<t:{round(datetime.datetime.now() + calc_cooldown)}:R>"
    # time until next work
    if last_work + calc_cooldown > datetime.datetime.now().timestamp():
        time_stamp = datetime.datetime.fromtimestamp(last_work + calc_cooldown)
        time_stamp = f'<t:{int(time_stamp.timestamp())}:R>'
        embed = discord.Embed(title="Work", description=f"Not so fast! You can work again {time_stamp}.\n{boost_message}", color=0xff0000)
        await ctx.reply(embed=embed)
    else:
        time_now = datetime.datetime.now()
        time_stamp = time_now + datetime.timedelta(seconds=calc_cooldown)
        time_stamp = f'<t:{int(time_stamp.timestamp())}:R>'
        earning_min = job_data['earning_min']
        earning_max = job_data['earning_max']
        earnings = random.randint(earning_min, earning_max)
        user_data['last_work'] = datetime.datetime.now().timestamp()
        user_data['coin_balance'] += earnings
        user_data['stats']['total_coinsearned'] += earnings
        user_data['stats']['total_works'] += 1
        user_data['stats']['works'][user_job] += 1
        user_data['stats']['seconds_worked'] += calc_cooldown
        if user_data['stats']['max_coins'] < user_data['coin_balance']:
            user_data['stats']['max_coins'] = user_data['coin_balance']
        user_data['hunger'] -= 1
        if user_data['hunger'] < 0:
            reply_answer = zero_hunger_message(user_data['id'])
            embed = discord.Embed(title="Fainted", color=0xff0000)
            embed.add_field(name="Hunger", value=f'2 / {user_data["hunger_max"]}')
            embed.add_field(name="Coins", value=f'{user_data["coin_balance"]}')
            embed.set_footer(text="Make sure to eat something using `|use [food]` to prevent this from happening again! Stock up on food by using `|shop food`.")
            await ctx.reply(reply_answer, embed=embed)
            return
        data_handler.save_user_data(user_id, user_data)
        random_work_messages = work_messages[user_data['work_job']]
        random_work_message = random.choice(random_work_messages)
        work_message = f"{random_work_message}\n\nYour earnings: <:coin:1273754255433531565> **{earnings}**\nYou can work again {time_stamp}.\n{boost_message}\n\nYour hunger bar has decreased by 1 point. Current hunger: {user_data['hunger']} / {user_data['hunger_max']}."
        embed = discord.Embed(title="Work", description=work_message, color=0x00ff00)
        if user_data['hunger'] == 0:
            work_message = f"{random_work_message}\n\nYour earnings: <:coin:1273754255433531565> **{earnings}**\nYou can work again {time_stamp}.\n{boost_message}\n\nYour hunger bar has decreased by 1 point. It is almost empty. Current hunger: {user_data['hunger']} / {user_data['hunger_max']}."
            embed = discord.Embed(title="Work", description=work_message, color=0xffff00)
            await ctx.reply("You are about to faint due to lack of hunger! Consider eating something using `|use [food]`. You will lose half of your coins if you faint.", embed=embed)
            return
        await ctx.reply(embed=embed)
        if user_data['settings']['work_cooldown_ping'] == True:
            message = await ctx.send(f"I will ping you when you can work again in {calc_cooldown} seconds.")
            await asyncio.sleep(calc_cooldown)
            await message.reply(f"{ctx.author.mention}, you can work again! Use `|work` to work again.\n-# If you don't want to be pinged when you can work again, use `|settings` and disable the work cooldown ping setting.")

@client.command()
async def bal(ctx, user: discord.Member = None, *args):
    if user is None:
        user = ctx.author

    user_id = user.id
    user_in_json = (data_handler.ensure_user_in_json(user_id) == "added")

    if user_in_json:
        if user == ctx.author:
            await ctx.reply(welcome_output)
        else:
            await ctx.reply("This user hasn't used the bot yet. Perhaps ask them to run a command?")
    else:
        user_data = data_handler.get_user_data(user_id)
        masked = False
        if 'mask_user' in user_data:
            user_id = user_data['mask_user']
            user_data = data_handler.get_user_data(user_id)
            print("MASKED USER AS ", user_id)
            masked = True
            user = await client.fetch_user(user_id)
        balance = user_data['coin_balance']
        bank_balance = user_data['bank_balance']
        bank_lvl = user_data['bank_lvl']
        user_publicname = user.display_name

        if user_id != ctx.author.id and not masked:
            bank_info = ""
        elif bank_lvl == 0:
            bank_info = f"""**Bank**
            You haven't unlocked the bank yet. See the `|shop` for more information."""
        else:
            bank_info = f"""**Bank**
            Bank Balance: {bank_balance}
            Bank Level: {bank_lvl}"""

        embed = discord.Embed(title=f"{user_publicname}'s Balance", 
                              description=f"""**Coin Balance**\n{balance}\n\n{bank_info}""", 
                              color=0x00ff00)
        embed.add_field(name="Total Earnings (Lifetime)", value=user_data['stats']['total_coinsearned'])
        embed.add_field(name="Hunger Bar", value=f"{user_data['hunger']} / {user_data['hunger_max']}")
        await ctx.reply(embed=embed)

@client.command()
async def inv(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    user_id = user.id
    user_in_json = data_handler.ensure_user_in_json(user_id)
    if user_in_json == "added":
        if user == ctx.author:
            await ctx.reply(welcome_output)
        else:
            await ctx.reply(f"{user.display_name} hasn't used the bot yet.")
        return
    elif user_in_json == "corrupted":
        await ctx.reply("# ERROR: Your user data is corrupted. Please contact the bot owner.\nThis is a fatal error and you have lost all of your data. Please DM <@1272666435063251057> **AS SOON AS POSSIBLE** for the possibility of restoring your data. This should hopefully never happen again. Thank you for your understanding.")

    user_data = data_handler.get_user_data(user_id)
    masked = False
    if 'mask_user' in user_data:
        user_id = user_data['mask_user']
        user_data = data_handler.get_user_data(user_id)
        masked = True
        print("MASKED USER AS ", user_id)
        user = await client.fetch_user(user_id)
    inventory_list = ''
    for item in user_data['inventory'].keys():
        inventory_list += f"* {id_to_name[item]} x{user_data['inventory'][item]}\n"

    embed = discord.Embed(
        title=f"{user.display_name}'s Inventory",
        description=f"Hunger Bar: {user_data['hunger']} / {user_data['hunger_max']}",
        color=0x00ff00
    )
    embed.add_field(name="Food Items", value=inventory_list or "No items")
    
    if user == ctx.author or masked:
        vehicle_list = "\n".join(f"* {id_to_name[vehicle]}" for vehicle in user_data['vehicles'])
        embed.add_field(name="Vehicles", value=vehicle_list or "No vehicles")
    
    embed.add_field(name="Current Vehicle", value=id_to_name.get(user_data['vehicle'], "None"))

    await ctx.reply(embed=embed)

@client.command()
async def dep(ctx, amount):
    user_id = ctx.author.id
    user_in_json = data_handler.ensure_user_in_json(user_id)
    if user_in_json == "added":
        await ctx.reply(welcome_output)
    else:
        user_data = data_handler.get_user_data(user_id)
        if 'mask_user' in user_data:
            user_id = user_data['mask_user']
            user_data = data_handler.get_user_data(user_id)
            user = await client.fetch_user(user_id)
        if user_data['bank_lvl'] == 0:
            await ctx.reply("You haven't unlocked the bank yet. See the `|shop` for more information.")
            return
        if amount.lower() == "all":
            amount = user_data['coin_balance']
            if amount == 0:
                await ctx.reply("You do not have any coins to deposit.")
                return
            if amount > bank_levels[user_data['bank_lvl']]['capacity'] - user_data['bank_balance']:
                amount = bank_levels[user_data['bank_lvl']]['capacity'] - user_data['bank_balance']
                if amount == 0:
                    await ctx.reply("Your bank is full. You cannot deposit any more coins. Consider upgrading your bank.")
                    return
                else:
                    user_data['coin_balance'] -= amount
                    user_data['bank_balance'] += amount
                    data_handler.save_user_data(user_id, user_data)
                    await ctx.reply(f"Deposited {amount} coins into your bank. Your bank balance is now {user_data['bank_balance']} / {bank_levels[user_data['bank_lvl']]['capacity']} coins.")
                    return
            else:
                user_data['coin_balance'] -= amount
                user_data['bank_balance'] += amount
                data_handler.save_user_data(user_id, user_data)
                await ctx.reply(f"Deposited {amount} coins into your bank. Your bank balance is now {user_data['bank_balance']} / {bank_levels[user_data['bank_lvl']]['capacity']} coins.")
                return
        else:
            if not amount.isdigit():
                await ctx.reply("Please enter a valid number to deposit.")
                return
            amount = int(amount)
            if user_data['bank_lvl'] == 0:
                await ctx.reply("You haven't unlocked the bank yet. See the `|shop` for more information.")
                return
            if amount <= 0:
                await ctx.reply("Please enter a valid number to deposit.")
                return
            if amount > user_data['coin_balance']:
                await ctx.reply("You do not have enough coins to deposit.")
                return
            if amount > bank_levels[user_data['bank_lvl']]['capacity'] - user_data['bank_balance']:
                amount = bank_levels[user_data['bank_lvl']]['capacity'] - user_data['bank_balance']
                if amount == 0:
                    await ctx.reply("Your bank is full. You cannot deposit any more coins. Consider upgrading your bank.")
                    return
                else:
                    await ctx.reply(f"There is not enough space in your bank to deposit {amount} coins.")
                    return
            user_data['coin_balance'] -= amount
            user_data['bank_balance'] += amount
            data_handler.save_user_data(user_id, user_data)
            await ctx.reply(f"Deposited {amount} coins into your bank. Your bank balance is now {user_data['bank_balance']} / {bank_levels[user_data['bank_lvl']]['capacity']} coins.")
            return

@client.command()
async def withdraw(ctx, amount):
    user_id = ctx.author.id
    user_in_json = data_handler.ensure_user_in_json(user_id)
    if user_in_json == "added":
        await ctx.reply(welcome_output)
    else:
        user_data = data_handler.get_user_data(user_id)
        if 'mask_user' in user_data:
            user_id = user_data['mask_user']
            user_data = data_handler.get_user_data(user_id)
            user = await client.fetch_user(user_id)
        if user_data['bank_lvl'] == 0:
            await ctx.reply("You haven't unlocked the bank yet. See the `|shop` for more information.")
            return
        if amount.lower() == "all":
            amount = user_data['bank_balance']
            if amount == 0:
                await ctx.reply("You do not have any coins to withdraw.")
                return
            user_data['coin_balance'] += amount
            user_data['bank_balance'] = 0
            data_handler.save_user_data(user_id, user_data)
            await ctx.reply(f"Withdrew {amount} coins from your bank. Your bank balance is now 0 / {bank_levels[user_data['bank_lvl']]['capacity']} coins.")
            return
        else:
            if not amount.isdigit():
                await ctx.reply("Please enter a valid number to withdraw.")
                return
            amount = int(amount)
            if amount <= 0:
                await ctx.reply("Please enter a valid number to withdraw.")
                return
            if user_data['bank_lvl'] == 0:
                await ctx.reply("You haven't unlocked the bank yet. See the `|shop` for more information.")
                return
            if amount > user_data['bank_balance']:
                await ctx.reply("You do not have enough coins to withdraw.")
                return
            user_data['coin_balance'] += amount
            user_data['bank_balance'] -= amount
            data_handler.save_user_data(user_id, user_data)
            await ctx.reply(f"Withdrew {amount} coins from your bank. Your bank balance is now {user_data['bank_balance']} / {bank_levels[user_data['bank_lvl']]['capacity']} coins.")
            return

@client.command(name='with')
async def withdraw_command(ctx, amount):
    await withdraw(ctx, amount)

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
            return
        elif shop_name.lower() == "vehicle" or shop_name.lower() == "vehicles" or shop_name.lower() == "car" or shop_name.lower() == "cars":
            await display_vehicle_shop(ctx)
            return
        elif shop_name.lower() == "special" or shop_name.lower() == "specials" or shop_name.lower() == "upgrades" or shop_name.lower() == "upgrade":
            await display_special_shop(ctx)
            return
        else:
            await ctx.send("Invalid shop name. Please use `|shop` to select a shop.")
            return
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
                    if item['id'] in user_data['inventory']:
                        user_data['inventory'][item['id']] += 1
                    else:
                        user_data['inventory'][item['id']] = 1
                    user_data['stats']['food_bought'] += 1
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
                if user_data['vehicle'] == item['id']:
                    await ctx.send(f"You already own and equipped {item['name']} as your active vehicle.")
                elif item['id'] in user_data['vehicles']:
                    user_data['vehicle'] = item['id']
                    data_handler.save_user_data(ctx.author.id, user_data)
                    await ctx.send(f"Equipped {item['name']} as your active vehicle.")
                elif user_data['coin_balance'] < item['price']:
                    await ctx.send("You do not have enough coins to purchase this vehicle.")
                else:
                    user_data['coin_balance'] -= item['price']
                    user_data['vehicles'].append(item['id'])
                    user_data['vehicle'] = item['id']
                    data_handler.save_user_data(ctx.author.id, user_data)
                    await ctx.send(f"You have purchased {item['name']} for {item['price']} coins! It is now your active vehicle.\n-# To switch vehicles, use the shop and click buy on the vehicle (it won't charge you again if you already own it).")
                await message.edit(embed=create_vehicle_embed(ctx.author.id, current_index))
        except Exception as e:
            break

upgrades = ["bank", "foodmeter", "shoes"]
def upgrade_shop_embed(user_id, shop_name, user_data):
    if shop_name == "bank":
        # get current bank level
        bank_lvl = user_data['bank_lvl']
        # get information about the current and next bank level
        current_bank_info = bank_levels[bank_lvl]
        if bank_lvl == len(bank_levels) - 1:
            embed = discord.Embed(
                title="Bank Account",
                description=f"The bank allows you to store coins safely and prevent them from being stolen. If you pass out from hunger, your bank balance will not be affected. If someone uses `|steal` on you, your bank balance is protected. Upgrade your bank to increase its capacity.",
                color=0x00ff00
            )
            embed.add_field(name="Current Level", value=f"{current_bank_info['description']}\n**Capacity**: {user_data['bank_balance']} / {current_bank_info['capacity']} coins")
            embed.add_field(name="Next Level", value="You have reached the maximum bank level. Check back later to see if more levels have been added.")
            embed.set_footer(text="Page 1 of 3")
            return embed
        next_bank_info = bank_levels[bank_lvl + 1]
        embed = discord.Embed(
            title="Bank Account",
            description=f"The bank allows you to store coins safely and prevent them from being stolen. If you pass out from hunger, your bank balance will not be affected. If someone uses `|steal` on you, your bank balance is protected. Upgrade your bank to increase its capacity.",
            color=0x00ff00
        )
        if current_bank_info['interest'] > 0:
            embed.add_field(name="Current Level", value=f"{current_bank_info['description']}\n**Capacity**: {user_data['bank_balance']} / {current_bank_info['capacity']} coins\n**Interest**: {current_bank_info['interest']*100}% per day")
        else:
            embed.add_field(name="Current Level", value=f"{current_bank_info['description']}\n**Capacity**: {user_data['bank_balance']} / {current_bank_info['capacity']} coins")
        if next_bank_info['interest'] > 0:
            embed.add_field(name="Next Level", value=f"{next_bank_info['description']}\n**Capacity**: {next_bank_info['capacity']} coins\n**Upgrade Cost**: {next_bank_info['price']} coins\n**Interest**: {next_bank_info['interest']*100}% per day")
        else:
            embed.add_field(name="Next Level", value=f"{next_bank_info['description']}\n**Capacity**: {next_bank_info['capacity']} coins\n**Upgrade Cost**: {next_bank_info['price']} coins")
        embed.set_footer(text="Page 1 of 3")
        return embed
    elif shop_name == "foodmeter":
        embed = discord.Embed(
            title="Food Meter",
            description="Every time you work, your food meter goes down by 1 point. If it reaches 0, you will faint and lose half of your coins and half of your inventory. Upgrade your food meter to increase its capacity and ensure you don't run out of food.",
            color=0x00ff00
        )
        user_maxhunger = user_data['hunger_max']
        hunger_level = user_maxhunger - 6
        current_hunger_info = hunger_levels[hunger_level]
        if hunger_level == len(hunger_levels) - 1:
            embed.add_field(name="Current Level", value=f"{current_hunger_info['description']}\n**Capacity**: {user_data['hunger']} / {user_maxhunger} points")
            embed.add_field(name="Next Level", value="You have reached the maximum food meter level. Check back later to see if more levels have been added.")
            embed.set_footer(text="Page 2 of 3")
            return embed
        next_hunger_info = hunger_levels[hunger_level + 1]
        embed.add_field(name="Current Level", value=f"{current_hunger_info['description']}\n**Capacity**: {user_data['hunger']} / {user_maxhunger} points")
        embed.add_field(name="Next Level", value=f"{next_hunger_info['description']}\n**Capacity**: {next_hunger_info['capacity']} points\n**Upgrade Cost**: {next_hunger_info['price']} coins")
        embed.set_footer(text="Page 2 of 3")
        return embed
    elif shop_name == "shoes":
        embed = discord.Embed(
            title="Coming soon...",
            description="Coming soon!",
            color=0x00ff00
        )
        embed.set_footer(text="Page 3 of 3")
        return embed

async def display_special_shop(ctx):
    current_index = 0
    message = await ctx.send(embed=upgrade_shop_embed(ctx.author.id, upgrades[current_index], data_handler.get_user_data(ctx.author.id)))

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
                await message.edit(embed=upgrade_shop_embed(ctx.author.id, upgrades[current_index], data_handler.get_user_data(ctx.author.id)))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '➡️':
                current_index = (current_index + 1) % len(special_shop_items)
                await message.edit(embed=upgrade_shop_embed(ctx.author.id, upgrades[current_index], data_handler.get_user_data(ctx.author.id)))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '💰':
                await message.remove_reaction(reaction, user)
                if upgrades[current_index] == "bank":
                    user_data = data_handler.get_user_data(ctx.author.id)
                    bank_lvl = user_data['bank_lvl']
                    if bank_lvl == len(bank_levels) - 1:
                        await ctx.send("You already have the maximum bank level. Check back later to see if more levels have been added.")
                    else:
                        next_bank_info = bank_levels[bank_lvl + 1]
                        if user_data['coin_balance'] < next_bank_info['price']:
                            await ctx.send("You do not have enough coins to upgrade your bank. Keep working to earn more coins!")
                        else:
                            user_data['coin_balance'] -= next_bank_info['price']
                            user_data['bank_lvl'] += 1
                            data_handler.save_user_data(ctx.author.id, user_data)
                            await message.edit(embed=upgrade_shop_embed(ctx.author.id, upgrades[current_index], data_handler.get_user_data(ctx.author.id)))
                            await ctx.send(f"You have upgraded your bank to level {bank_lvl + 1}!")
                elif upgrades[current_index] == "foodmeter":
                    user_data = data_handler.get_user_data(ctx.author.id)
                    user_maxhunger = user_data['hunger_max']
                    hunger_level = user_maxhunger - 6
                    if hunger_level == len(hunger_levels) - 1:
                        await ctx.send("You already have the maximum food meter level. Check back later to see if more levels have been added.")
                    else:
                        next_hunger_info = hunger_levels[hunger_level + 1]
                        if user_data['coin_balance'] < next_hunger_info['price']:
                            await ctx.send("You do not have enough coins to upgrade your food meter. Keep working to earn more coins!")
                        else:
                            user_data['coin_balance'] -= next_hunger_info['price']
                            user_data['hunger_max'] += 1
                            data_handler.save_user_data(ctx.author.id, user_data)
                            await message.edit(embed=upgrade_shop_embed(ctx.author.id, upgrades[current_index], data_handler.get_user_data(ctx.author.id)))
                            await ctx.send(f"You have upgraded your food meter to level {hunger_level + 1}! Food not included. Buy food from the shop to fill that expanded hunger meter! Your current hunger bar: {user_data['hunger']} / {user_data['hunger_max']}")
        except Exception as e:
            print(e)
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

quick_shop_items = {
    "sausage": 10,
    "orange": 20,
    "burger": 50,
    "spaghetti": 100,
}

@client.command()
async def use(ctx, item_name):
    user_data = data_handler.get_user_data(ctx.author.id)
    inventory = user_data['inventory']
    if item_name not in inventory:
        if user_data['settings']['auto_buy'] == True:
            if item_name in quick_shop_items:
                price = quick_shop_items[item_name]
                if user_data['coin_balance'] < price:
                    await ctx.send(f"You don't have a {id_to_name[item_name]} in your inventory and you don't have enough coins to buy it either.")
                    return
                user_data['coin_balance'] -= price
                refill = food_hunger_refill[item_name]
                user_data['hunger'] += refill
                if user_data['hunger'] > user_data['hunger_max']:
                    user_data['hunger'] = user_data['hunger_max']
                embed = discord.Embed(title="Tasty!", color=0x00ff00)
                embed.add_field(name="Hunger", value=f"{user_data['hunger']} / {user_data['hunger_max']}")
                embed.add_field(name="Food Consumed", value=id_to_name[item_name])
                user_data['stats']['food_eaten'] += 1
                data_handler.save_user_data(ctx.author.id, user_data)
                await ctx.send(f"You bought a {id_to_name[item_name]} for {price} coins and ate it, which refilled your hunger by {refill} points. Your hunger bar is now at {user_data['hunger']} points.\n-# You have automatically spent {price} coins due to your Auto Buy setting. Run `|settings` to change this behavior.", embed=embed)
                return
            await ctx.send(f"You do not have {id_to_name[item_name]} in your inventory. Maybe you can buy it from the shop?")
            return
        await ctx.send(f"You do not have {id_to_name[item_name]} in your inventory. Maybe you can buy it from the shop?")
        return
    # item must be in inventory
    item_type = item_type_from_id[item_name]
    if item_type == "food" or item_type == "debug":
        refill = food_hunger_refill[item_name]
        user_data['hunger'] += refill
        if user_data['hunger'] > user_data['hunger_max']:
            user_data['hunger'] = user_data['hunger_max']
        user_data["inventory"][item_name] -= 1
        if user_data["inventory"][item_name] == 0:
            del user_data["inventory"][item_name]
        embed = discord.Embed(title="Tasty!", color=0x00ff00)
        embed.add_field(name="Hunger", value=f"{user_data['hunger']} / {user_data['hunger_max']}")
        embed.add_field(name="Food Consumed", value=id_to_name[item_name])
        user_data['stats']['food_eaten'] += 1
        data_handler.save_user_data(ctx.author.id, user_data)
        await ctx.send(f"You ate a {id_to_name[item_name]} and refilled your hunger by {refill} points. Your hunger bar is now at {user_data['hunger']} points.", embed=embed)
    else:
        await ctx.send("That item is not usable or does not exist. Perhaps check your spelling?")

@client.command()
async def eat(ctx, item_name):
    await use(ctx, item_name)


@client.command()
async def buy(ctx, item_name, amount=1):
    user_data = data_handler.get_user_data(ctx.author.id)
    if item_name in quick_shop_items:
        price = quick_shop_items[item_name]
    else:
        await ctx.send("That item does not exist in the quick shop. Please use the regular shop to buy that.")
        return
    if user_data['coin_balance'] < price * amount:
        await ctx.send(f"You do not have enough coins to buy that item. It costs {price * amount} coins.")
        return
    user_data['coin_balance'] -= price * amount
    if item_name in user_data['inventory']:
        user_data['inventory'][item_name] += amount
    else:
        user_data['inventory'][item_name] = amount
    data_handler.save_user_data(ctx.author.id, user_data)
    await ctx.send(f"You have purchased {amount} {id_to_name[item_name]} for {price * amount} coins!")

@client.command()
async def help(ctx, command=None):
    if command:
        command = command.lower()
        if command in command_help:
            embed = discord.Embed(
                title=f"Help - {command}",
                description=command_help[command],
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("That command does not exist. Please check the command and try again.")
        return
    embed = discord.Embed(
        title="Sasbot Help",
        description=help_output,
    )
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    # Create a base embed for error messages
    embed = discord.Embed(title="Error", color=discord.Color.red())

    if isinstance(error, commands.CommandNotFound):
        embed.description = f"The command `{ctx.invoked_with}` does not exist. Please check the command and try again."
    
    elif isinstance(error, commands.MemberNotFound):
        embed.description = f"The member `{error.argument}` could not be found. Please ensure the username or mention is correct."
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.description = f"You're missing a required argument: `{error.param.name}`. Please provide it and try again."
    
    elif isinstance(error, commands.BadArgument):
        embed.description = f"You provided an invalid argument for the command `{ctx.command}`. Please check your input and try again."
    
    elif isinstance(error, commands.MissingPermissions):
        embed.description = f"You don't have the necessary permissions to run the command `{ctx.command}`."
    
    elif isinstance(error, commands.BotMissingPermissions):
        embed.description = f"I don't have the necessary permissions to execute the command `{ctx.command}`. Please check my permissions and try again."
    
    elif isinstance(error, commands.NotOwner):
        embed.description = "This command can only be used by the bot owner."
    
    elif isinstance(error, commands.CommandOnCooldown):
        embed.description = f"The command `{ctx.command}` is on cooldown. Please try again after {error.retry_after:.2f} seconds."
    
    elif isinstance(error, commands.CheckFailure):
        embed.description = f"You do not meet the requirements to use the command `{ctx.command}`."
    
    else:
        embed.description = f"An unexpected error occurred while processing the command `{ctx.command}`."
        raise error  # Re-raise the error for further logging or debugging if needed

    # Send the embed with the error message
    await ctx.reply(embed=embed)

@client.command()
async def reset(ctx):
    message = await ctx.reply("**DANGER ZONE**\nThis command will reset all of your data. Are you sure you want to proceed?")
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['✅', '❌']
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)
        if str(reaction.emoji) == '✅':
            message = await ctx.reply("Are you absolutely sure you want to reset all of your data? This action is irreversible. You will lose all of your coins, items, and progress. The data cannot be recovered under any circumstances. If you proceed, you will be starting from scratch and forfeit any current progress. Additionally, you will lose any special ranks, items, or perks you may have obtained. This includes Early Tester role, bank levels and contents, and any other special roles or items. Are you sure you want to proceed?")
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            def check(reaction, user):
                return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['✅', '❌']
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)
                if str(reaction.emoji) == '✅':
                    user_data = data_handler.get_user_data(ctx.author.id)
                    print(user_data)
                    user_data_base64 = base64.b64encode(str(user_data).encode('utf-8')).decode('utf-8')
                    secret_key = os.getenv('SECRET_KEY')
                    secret_key = secret_key.encode('utf-8')
                    print(secret_key)
                    f = Fernet(secret_key)
                    encrypted_user_data = f.encrypt(user_data_base64.encode('utf-8'))
                    print(encrypted_user_data)
                    data_handler.drop_user(ctx.author.id)
                    embed = discord.Embed(title="Data Reset", description=f"Your data has been deleted from our servers completely. Thank you for using Sasbot and we hope you return! If you already regret losing this data, your recovery phrase is below.\n\n```\n{encrypted_user_data.decode('utf-8')}\n```", color=0xff0000)
                    # embed.set_footer(text=f"Recovery Phrase: {encrypted_user_data}")
                    # embed.add_field(name="Recovery Phrase", value=f"```{str(encrypted_user_data)}```")
                    await ctx.reply("Your data has been reset. You are now starting from scratch.", embed=embed)
                else:
                    await ctx.send("Reset cancelled.")
            except Exception as e:
                print(e)
                await ctx.send("Reset cancelled.")
        else:
            await ctx.send("Reset cancelled.")
    except Exception as e:
        await ctx.send("Reset cancelled.")

@client.command()
async def restore(ctx, user, string):
    string = string.encode('utf-8')
    secret_key = os.getenv('SECRET_KEY')
    secret_key = secret_key.encode('utf-8')
    f = Fernet(secret_key)
    decrypted_user_data = f.decrypt(string).decode('utf-8')
    user_data = ast.literal_eval(decrypted_user_data)
    data_handler.save_user_data(user, user_data)
    await ctx.send("User data restored.")
    

@client.command()
async def debug(ctx, command, user: discord.Member = None, *args):
    if ctx.guild is None:
        await ctx.send(f"Nice try. Your User ID is clearly {ctx.author.id} which does not match my owner's. Please never try this command again.", embed=bot_dm_embed)
        return
    elif ctx.author.id == 773996537414942763:
        commands = ["cooldown", "foodmeter", "job", "vehicle", "banklvl", "hungerlvl", "reset_debug_DANGER", "save_data", "get_stat"]
        if command not in commands:
            embed = discord.Embed(title="Error", description="This command does not exist. Pinky promise.", color=0x00ffff)
            await ctx.send("Command not found! Error! Don't run this anymore!", embed=embed)
            return
        if user is None:
            user = ctx.author
        if command == "cooldown":
            user_data = data_handler.get_user_data(user.id)
            user_data['last_work'] = int(args[0])
            data_handler.save_user_data(user.id, user_data)
            await ctx.send(f"Cooldown for {user.id} set to {args[0]}")
            return
        elif command == "foodmeter":
            user_data = data_handler.get_user_data(user.id)
            user_data['hunger'] = int(args[0])
            data_handler.save_user_data(user.id, user_data)
            await ctx.send(f"Food meter for {user.id} set to {args[0]}")
            return
        elif command == "job":
            user_data = data_handler.get_user_data(user.id)
            user_data['work_job'] = args[0]
            data_handler.save_user_data(user.id, user_data)
            await ctx.send(f"Job for {user.id} set to {args[0]}")
            return
        elif command == "vehicle":
            user_data = data_handler.get_user_data(user.id)
            user_data['vehicle'] = args[0]
            data_handler.save_user_data(user.id, user_data)
            await ctx.send(f"Vehicle for {user.id} set to {args[0]}")
            return
        elif command == "banklvl":
            user_data = data_handler.get_user_data(user.id)
            user_data['bank_lvl'] = int(args[0])
            data_handler.save_user_data(user.id, user_data)
            await ctx.send(f"Bank level for {user.id} set to {args[0]}")
            return
        elif command == "hungerlvl":
            user_data = data_handler.get_user_data(user.id)
            user_data['hunger_max'] = int(args[0])
            data_handler.save_user_data(user.id, user_data)
            await ctx.send(f"Hunger level for {user.id} set to {args[0]}")
            return
        elif command == "reset_debug_DANGER":
            data_handler.drop_user(user.id)
            await ctx.send(f"User {user.id} has removed from the database.")
            return
        elif command == "save_data":
            user_data = data_handler.get_user_data(user.id)
            user_data_base64 = base64.b64encode(str(user_data).encode('utf-8')).decode('utf-8')
            secret_key = os.getenv('SECRET_KEY')
            secret_key = secret_key.encode('utf-8')
            print(secret_key)
            f = Fernet(secret_key)
            encrypted_user_data = f.encrypt(user_data_base64.encode('utf-8'))
            print(encrypted_user_data)
            await ctx.send(f"Debug User Data: {encrypted_user_data.decode('utf-8')}")
            return
        elif command == "get_stat":
            user_data = data_handler.get_user_data(user.id)
            await ctx.send(f"{user.id} has {user_data['stats'][args[0]]} {args[0]}")
    else:
        embed = discord.Embed(title="Error", description="This command does not exist. Pinky promise.", color=0x00ffff)
        await ctx.send("Command not found! Error! Don't run this anymore!", embed=embed)

@client.command()
async def mask(ctx, user: discord.Member = None):
    if ctx.author.id == 773996537414942763:
        if user is None:
            user_data = data_handler.get_user_data(ctx.author.id)
            if 'mask_user' in user_data:
                del user_data['mask_user']
                data_handler.save_user_data(ctx.author.id, user_data)
                await ctx.send("You have been unmasked.")
            return
        user_data = data_handler.get_user_data(ctx.author.id)
        user_data['mask_user'] = user.id
        data_handler.save_user_data(ctx.author.id, user_data)
        await ctx.send(f"You have been masked as {user.id}.")
        return
    else:
        error = discord.Embed(title="Error", description="This command does not exist. Pinky promise.", color=0x00ffff)
        await ctx.send("Command not found! Error! Don't run this anymore!", embed=error)
        return

bad_words = []
# load bad words from file which are base64 encoded because the code is open source
with open("badwords.txt", "r") as f:
    base64_bad_words = f.read()
    bad_words = base64.b64decode(base64_bad_words).decode('utf-8').split("\n")

@client.event
async def on_message(ctx):
    if ctx.author.bot:
        return
    if ctx.guild is None and ctx.author.id != 773996537414942763:
        await ctx.reply("This bot will not work in DMs. Consider adding it to your server.", embed=bot_dm_embed)
        return
    if ctx.channel.id != 1279662904806998147 and os.environ.get('DEBUG') == "True":
        return
    user_data = data_handler.get_user_data(ctx.author.id)
    for badword in bad_words:
        if badword in ctx.content.lower():
            if user_data['settings']['detect_bad_words'] == True:
                await ctx.reply("Bad word detected!")
            user_data['stats']['bad_words'] += 1
            data_handler.save_user_data(ctx.author.id, user_data)
            return
    await client.process_commands(ctx)        

@client.command()
async def sell(ctx, item_name, amount=1):
    user_data = data_handler.get_user_data(ctx.author.id)
    if item_name == 'all':
        total_price = 0
        print(user_data['inventory'])
        for i in range(len(user_data['inventory'])):
            print(f"selling {user_data['inventory'][i]} for {quick_shop_items[user_data['inventory'][i]]//2}")
            price = quick_shop_items[user_data['inventory'][i]]//2
            total_price += price
        user_data['coin_balance'] += total_price
        user_data['inventory'] = []
        if user_data['coin_balance'] > user_data['stats']['max_coins']:
            user_data['stats']['max_coins'] = user_data['coin_balance']
        data_handler.save_user_data(ctx.author.id, user_data)
        await ctx.send(f"You have sold all of your items for {total_price} coins!")
        return
    if item_name not in user_data['inventory']:
        await ctx.send(f"You do not have {id_to_name[item_name]} in your inventory.")
        return
    if amount > user_data['inventory'].count(item_name):
        await ctx.send(f"You do not have {amount} {id_to_name[item_name]} in your inventory.")
        return
    price = quick_shop_items[item_name]//2
    user_data['coin_balance'] += price * amount
    for _ in range(amount):
        user_data['inventory'].remove(item_name)
    if user_data['coin_balance'] > user_data['stats']['max_coins']:
        user_data['stats']['max_coins'] = user_data['coin_balance']
    data_handler.save_user_data(ctx.author.id, user_data)
    await ctx.send(f"You have sold {amount} {id_to_name[item_name]} for {price * amount} coins!")

def generate_settings_embed(user_id):
    user_data = data_handler.get_user_data(user_id)
    if 'mask_user' in user_data:
        user_id = user_data['mask_user']
        user_data = data_handler.get_user_data(user_id)
    user_settings = user_data['settings']
    embed = discord.Embed(
        title="User Settings",
        description="There are currently 3 settings you can toggle on or off. Use the associated reactions to toggle the settings.",
        color=0x00ff00
    )
    if user_settings['detect_bad_words'] == True:
        embed.add_field(name="Detect Bad Words 🤬", value="Uses the bad word detection filter from in game to ping you whenever you send an offending message!\nEnabled ✅")
    else:
        embed.add_field(name="Detect Bad Words 🤬", value="Uses the bad word detection filter from in game to ping you whenever you send an offending message!\nDisabled ❌")
    if user_settings['interest_dm'] == True:
        embed.add_field(name="Interest DMs 🔔", value="Receive a direct message when you earn interest on your bank balance each night at 00:00 PST.\nEnabled ✅")
    else:
        embed.add_field(name="Interest DMs 🔔", value="Receive a direct message when you earn interest on your bank balance each night at 00:00 PST.\nDisabled ❌")
    if user_settings['auto_buy'] == True:
        embed.add_field(name="Auto Buy 💰", value="Forget about buying food! When you run `|eat` and don't have the food item in your inventory, it will automatically buy it.\nEnabled ✅")
    else:
        embed.add_field(name="Auto Buy 💰", value="Forget about buying food! When you run `|eat` and don't have the food item in your inventory, it will automatically buy it.\nDisabled ❌")
    embed.set_footer(text="Page 1 of 1")
    return embed

@client.command()
async def settings(ctx):
    # create an embed with the user's settings and allow them to toggle switches using reactions
    user_data = data_handler.get_user_data(ctx.author.id)
    message = await ctx.send(embed=generate_settings_embed(ctx.author.id))
    await message.add_reaction('🤬')
    await message.add_reaction('🔔')
    await message.add_reaction('💰')
    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['🤬', '💰', '🔔']
    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            await message.remove_reaction(reaction, user)
            if str(reaction.emoji) == '🤬':
                user_data['settings']['detect_bad_words'] = not user_data['settings']['detect_bad_words']
            elif str(reaction.emoji) == '🔔':
                user_data['settings']['interest_dm'] = not user_data['settings']['interest_dm']
            elif str(reaction.emoji) == '💰':
                user_data['settings']['auto_buy'] = not user_data['settings']['auto_buy']
            data_handler.save_user_data(ctx.author.id, user_data)
            await message.edit(embed=generate_settings_embed(ctx.author.id))
        except Exception as e:
            break

@client.command()
async def stats(ctx, stat_book=None, user: discord.Member = None):
    if user is None:
        user = ctx.author
    user_id = user.id
    user_data = data_handler.get_user_data(user_id)
    if 'mask_user' in user_data:
        user_id = user_data['mask_user']
        user_data = data_handler.get_user_data(user_id)
    display_name = user.display_name
    if stat_book is None:
        embed = discord.Embed(
            title=f"{display_name}'s Stats",
            description="Select a reaction to view different categories of stats.",
            color=0x00ff00
        )
        embed.add_field(name="Coin Stats 🪙", value="View stats related to coins and the economy.")
        embed.add_field(name="Work Stats 💼", value="View stats related to working and jobs.")
        embed.add_field(name="Misc Stats 📊", value="View miscellaneous stats.")
        message = await ctx.send(embed=embed)
        await message.add_reaction('🪙')
        await message.add_reaction('💼')
        await message.add_reaction('📊')
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['🪙', '💼', '📊']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                await message.remove_reaction(reaction, user)
                if str(reaction.emoji) == '🪙':
                    await message.delete()
                    await stats(ctx, "coin")
                    return
                elif str(reaction.emoji) == '💼':
                    await message.delete()
                    await stats(ctx, "work")
                    return
                elif str(reaction.emoji) == '📊':
                    await message.delete()
                    await stats(ctx, "misc")
                    return
            except Exception as e:
                break
    if stat_book == "coin":
        user_stats = user_data['stats']
        stats_list = ["total_coinsearned", "max_coins", "interest_earned"]
        embed = discord.Embed(
            title=f"{display_name}'s Coin Stats",
            description="View stats related to coins and the economy.",
            color=0x00ff00
        )
        for stat in stats_list:
            embed.add_field(name=id_to_name[stat], value=user_stats[stat])
        message = await ctx.send(embed=embed)
        await message.add_reaction('🪙')
        await message.add_reaction('💼')
        await message.add_reaction('📊')
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['🪙', '💼', '📊']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                await message.remove_reaction(reaction, user)
                if str(reaction.emoji) == '🪙':
                    await ctx.send("You are already viewing coin stats.")
                elif str(reaction.emoji) == '💼':
                    await message.delete()
                    await stats(ctx, "work")
                    return
                elif str(reaction.emoji) == '📊':
                    await message.delete()
                    await stats(ctx, "misc")
                    return
            except Exception as e:
                break
    elif stat_book == "work":
        user_stats = user_data['stats']
        embed = discord.Embed(
            title=f"{display_name}'s Work Stats",
            description=f"Total Works: {user_stats['total_works']}\nSeconds Worked: {user_stats['seconds_worked']}\nWorks per job:",
            color=0x00ff00
        )
        for job in jobs_list:
            embed.add_field(name=id_to_name[job], value=user_stats['works'][job])
        message = await ctx.send(embed=embed)
        await message.add_reaction('🪙')
        await message.add_reaction('💼')
        await message.add_reaction('📊')
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['🪙', '💼', '📊']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                await message.remove_reaction(reaction, user)
                if str(reaction.emoji) == '🪙':
                    await message.delete()
                    await stats(ctx, "coin")
                    return
                elif str(reaction.emoji) == '💼':
                    await ctx.send("You are already viewing work stats.")
                elif str(reaction.emoji) == '📊':
                    await message.delete()
                    await stats(ctx, "misc")
                    return
            except Exception as e:
                print(e)
                break
    elif stat_book == "misc":
        user_stats = user_data['stats']
        embed = discord.Embed(
            title=f"{display_name}'s Misc Stats",
            description="View miscellaneous stats.",
            color=0x00ff00
        )
        stats_list = ["food_eaten", "food_bought", "bad_words"]
        for stat in stats_list:
            embed.add_field(name=id_to_name[stat], value=user_stats[stat])
        message = await ctx.send(embed=embed)
        await message.add_reaction('🪙')
        await message.add_reaction('💼')
        await message.add_reaction('📊')
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['🪙', '💼', '📊']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                await message.remove_reaction(reaction, user)
                if str(reaction.emoji) == '🪙':
                    await message.delete()
                    await stats(ctx, "coin")
                    return
                elif str(reaction.emoji) == '💼':
                    await message.delete()
                    await stats(ctx, "work")
                    return
                elif str(reaction.emoji) == '📊':
                    await ctx.send("You are already viewing miscellaneous stats.")
            except Exception as e:
                break

@tasks.loop(hours=24)
async def apply_interest():
    users = data_handler.get_all_users()
    for user_id in users:
        user_data = data_handler.get_user_data(user_id)
        bank_lvl = user_data['bank_lvl']
        interest = bank_levels[bank_lvl]['interest']
        print(f"Applying {interest}% interest to {user_id}'s bank balance.")
        if interest > 0:
            user_data['stats']['interest_earned'] += user_data['bank_balance'] * (interest / 100)
            user_data['bank_balance'] += user_data['bank_balance'] * (interest / 100)
            if user_data['bank_balance'] > bank_levels[bank_lvl]['capacity']:
                user_data['bank_balance'] = bank_levels[bank_lvl]['capacity']
                user = await client.fetch_user(user_id)
                data_handler.save_user_data(user_id, user_data)
                await user.send(f"Your bank balance has been increased by {interest}% interest. However, your bank balance has reached its maximum capacity of {bank_levels[bank_lvl]['capacity']} coins. Please upgrade your bank to increase its capacity or withdraw coins.")
                break
            user_data['coin_balance'] = round(user_data['coin_balance'])
            user_data['bank_balance'] = round(user_data['bank_balance'])
            data_handler.save_user_data(user_id, user_data)
            user = await client.fetch_user(user_id)
            if user_data['settings']['interest_dm'] == True:
                await user.send(f"Your bank balance has been increased by {interest*100}% interest. Your new balance is {user_data['bank_balance']} / {bank_levels[user_data['bank_lvl']]['capacity']} coins.")

async def wait_until_midnight_pst():
    tz = pytz.timezone('US/Pacific')
    now = datetime.datetime.now(tz)
    # Calculate time until the next 00:00 PST
    next_midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # next_midnight = (now + datetime.timedelta(seconds=20))
    time_until_midnight = (next_midnight - now).total_seconds()
    print(f"Waiting until midnight PST ({next_midnight}) in {time_until_midnight} seconds")
    await asyncio.sleep(time_until_midnight)
    apply_interest.start()

@client.command()
async def give(ctx, member: discord.Member, amount: int, type="coins"):
    user_id = ctx.author.id
    user_data = data_handler.get_user_data(user_id)
    if 'mask_user' in user_data:
        user_id = user_data['mask_user']
        user_data = data_handler.get_user_data(user_id)
        print(f"Masked user: {user_id}")
    if ctx.author.id == 773996537414942763:
        if type == "coins":
            user_data = data_handler.get_user_data(member.id)
            user_data['coin_balance'] += amount
            data_handler.save_user_data(member.id, user_data)
            await ctx.send(f"Added {amount} coins to {member.mention}'s account.")
            return
        type_ = item_type_from_id[type]
        if type_ == "food":
            user_data = data_handler.get_user_data(member.id)
            for _ in range(amount):
                user_data['inventory'].append(type)
            data_handler.save_user_data(member.id, user_data)
            await ctx.send(f"Gave {member.mention} {amount} {id_to_name[type]}.")
            return
        if type_ == "vehicle" or type == "debug":
            user_data = data_handler.get_user_data(member.id)
            user_data['vehicles'].append(type)
            if amount == -1:
                user_data['vehicle'] = type
                await ctx.send(f"Gave {member.mention} {id_to_name[type]}. Equipped.")
            elif amount == 0:
                # remove vehicle
                user_data['vehicles'].remove(type)
                if user_data['vehicle'] == type:
                    user_data['vehicle'] = None
                    await ctx.send(f"Removed {member.mention}'s {id_to_name[type]}. Unequipped.")
                else:
                    await ctx.send(f"Removed {member.mention}'s {id_to_name[type]}. Was not equipped.")
            else:
                await ctx.send(f"Gave {member.mention} {id_to_name[type]}. Not equipped.")
            data_handler.save_user_data(member.id, user_data)
            return
        await ctx.send("That item type does not exist. Please check your spelling and try again.")
    else:
        # ignore type, only allow coins
        if type == "coins":
            if amount > user_data['coin_balance']:
                await ctx.send("You do not have enough coins to give that amount.")
                return
            if amount < 0:
                await ctx.send("You cannot give a negative amount of coins.")
                return
            user_data = data_handler.get_user_data(member.id)
            user_data['coin_balance'] += amount
            data_handler.save_user_data(member.id, user_data)
            user_data = data_handler.get_user_data(user_id)
            user_data['coin_balance'] -= amount
            data_handler.save_user_data(user_id, user_data)
            await ctx.send(f"Gave {member.mention} {amount} coins. You now have {user_data['coin_balance']} coins.")
            return
        return

@client.command()
async def leaderboard(ctx):
    users = data_handler.get_all_users()
    leaderboard = []
    for user_id in users:
        user_data = data_handler.get_user_data(user_id)
        leaderboard.append((user_data['coin_balance'], user_id))
    leaderboard.sort(reverse=True)
    leaderboard_str = ''
    for i, (balance, user_id) in enumerate(leaderboard[:10]):
        user = await client.fetch_user(user_id)
        leaderboard_str += f"{i+1}. {user.name} - {balance} coins\n"
    embed = discord.Embed(
        title="Leaderboard",
        description="The top 10 users by coin balance:\n" + leaderboard_str,
        color=0x00ff00
    )
    embed.set_footer(text="Keep making coins to climb the leaderboard!")
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    print(f'{client.user} is connected and ready!')
    await wait_until_midnight_pst()

client.run(os.getenv('TOKEN'))