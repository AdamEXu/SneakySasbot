import discord

# Migration utilities for updating user data versions
current_user_data_version = 5

help_output = """
This is Adam The Great's interpretation of Sasbot. It contains an economy, and some fun commands.

For more information on a specific command, run `|help [command]`.

**ECONOMY**
Make money using `|work`
Explore other jobs using `|jobs`
Buy food, vehicles, and more in the shop with `|shop`
Check how many coins you have with `|bal`
See your inventory with `|inv`
Eat food to refill your hunger bar with `|use [food]`
To quickly buy food, use `|buy [food] [amount]`
Deposit your coins in the bank with `|dep [amount]`
Withdraw your coins from the bank with `|with [amount]`

**FUN**
~~View a random Sneaky Sasquatch meme with `|meme` ||If you would like to submit a meme, DM <@773996537414942763>.||~~
Coming soon!

**UTILITY**
To change your settings, use `|settings`

If you encounter any problems at all whatsoever, ping <@773996537414942763>.
-# Version 1.0.0
"""

welcome_output = f"""
Thank you for testing out this bot! It is currently a really early proof of concept. Many features are missing, and the bot is overall pretty buggy. 

To start making coins, run `|work`.
Keep an eye on your hunger bar! If it hits 0, there will be consequences. To fill it, run `|eat [food]`, where food is the name of the food you want to eat.
To see what is in your inventory (and see what food you have to eat), run `|inv`.

Take a look at `|help` for more information. If you encounter any problems at all whatsoever, ping <@773996537414942763>. (Yes I just pinged myself)
"""

food_shop_items = [
  {
    "id": "sausage",
    "name": "Sausage",
    "description": "A random sausage from the campground. Heals the hunger bar by 1 point.",
    "price": 10,
  },
  {
    "id": "orange",
    "name": "Orange",
    "description": "The holy orange, fresh from the supermarket. Heals the hunger bar by 2 points.",
    "price": 20,
  },
  {
    "id": "burger",
    "name": "Burger",
    "description": "Made to order with fresh ingredients at the diner. Heals the hunger bar by 5 points.",
    "price": 50,
  },
  {
    "id": "spaghetti",
    "name": "Spaghetti",
    "description": "Fresh from the Spaghetti Hotline. Heals the hunger bar all the way.",
    "price": 100,
  }
]

vehicle_shop_items = [
  {
    "id": "golfcart",
    "name": "Golf Cart",
    "description": "A slow vehicle, but faster than running. Reduces the cooldown for work by 5%.",
    "price": 200,
    "modifier": 0.95
  },
  {
    "id": "car",
    "name": "Car",
    "description": "A trusty vehicle, this car will last for 50 years! Reduces the cooldown for work by 10%.",
    "price": 250,
    "modifier": 0.9
  },
  {
    "id": "sports",
    "name": "Sports Car",
    "description": "Great for racing, and amazing value. Reduces the cooldown for work by 20%",
    "price": 500,
    "modifier": 0.8
  },
  {
    "id": "super",
    "name": "Super Car",
    "description": "This is probably the fastest you will need. Reduces the cooldown for work by 30%.",
    "price": 2500,
    "modifier": 0.7
  },
  {
    "id": "bike",
    "name": "Super Bike",
    "description": "In the real game, the super bike is certainly overpriced and not that much faster than the super car. But I'm generous. Reduces the cooldown for work by 50%.",
    "price": 50000,
    "modifier": 0.5
  }
]

special_shop_items = [
  "bank",
  "food_meter",
  "shoes"
]

id_to_name = {
  "": "None",
  "sausage": "Sausage",
  "orange": "Orange",
  "burger": "Burger",
  "spaghetti": "Spaghetti",
  "golfcart": "Golf Cart",
  "car": "Car",
  "sports": "Sports Car",
  "super": "Super Car",
  "bike": "Super Bike",
  "bank": "Bank Account Upgrade",
  "food_meter": "Bigger Food Meter",
  "shoes": "Shoes Upgrade",
  "debug": "Debug Item",
  "campground": "Food Stealer",
  "fishing": "Fisher",
  "taxi": "Taxi Driver",
  "delivery": "Delivery Person",
  "newspaper": "Photographer",
  "paramedic": "Paramedic",
  "police": "Police Officer",
  "doctor": "Doctor",
  "ferry": "Ferry Driver",
  "trash": "Trash Diver",
  "mushroom": "Mushroom Collector",
  "port": "Port Robber",
  "total_coinsearned": "Total Coins Earned",
  "max_coins": "Highest Coin Balance",
  "interest_earned": "Interest Earned (from bank)",
  "food_eaten": "Food Eaten",
  "food_bought": "Food Bought",
  "bad_words": "Bad Words Said",
}

jobs_list = ["campground", "fishing", "taxi", "delivery", "newspaper", "paramedic", "police", "doctor", "ferry", "trash", "mushroom", "port"]

work_messages = {
  "campground": ["You found a cooler with some food in it and sold it to the bear.", "You took some food from a grill and sold it to the bear.", "You found some food in a fridge in a RV and sold it to the bear.", "You found some food in a tent and sold it to the bear.", "You found some food in the ranger station and sold it to the bear.", "You found some food in a picnic basket and sold it to a bear."],
  "fishing": ["You caught a fish and sold it to the bear.", "Nice fishing session, you found a stergeon! (RARE FIND)", "Wow, you found a GOLD FISH and sold it to the bear! (RARE FIND)", "You found a minnow and sold it to the bear.", "You found a trout and sold it to the bear.", "You caught a sunfish and sold it to the bear.", "You caught a catfish and sold it to the bear.", "You caught a crappie and sold it to the bear.", "You caught a bass and sold it to the bear.", "You caught a perch and sold it to the bear.", "You caught a suckerfish and sold it to the bear.", "You caught a bass and sold it to the bear.", "You caught a sculpin and sold it to the bear.", "You caught a stickleback and sold it to the bear.", "You caught a kokanee and sold it to the bear.", "You caught a lamprey and sold it to the bear.", "You caught a carp and sold it to the bear.", "You caught a greyling and sold it to the bear.", "You caught a whitefish and sold it to the bear.", "You caught a salmon and sold it to the bear.", "You caught a burbot and sold it to the bear.", "You caught a dolly varden and sold it to the bear.", "You caught a shad and sold it to the bear.", "You caught a pike and sold it to the bear.", "You caught a crayfish and sold it to the bear.", "You caught a cavefish and sold it to the bear.", "You caught a minnow and sold it to the bear.", "You caught a trout and sold it to the bear.", "You cuaght a sculpin and sold it to the bear.", "You caught a sunfish and sold it to the bear.", "You caught a carp and sold it to the bear."],
  "taxi": ["You drove someone to the campground.", "You drove someone to the town.", "You drove someone to the golf course.", "You drove someone to the ski lodge.", "You drove someone to the race track."],
  "delivery": ["You delivered a package and earned some coins.", "You delivered a letter and earned some coins.", "You delivered an envolope and earned some coins."],
  "newspaper": ["You took a picture of a Sasquatch and earned some coins."],
  "paramedic": ["You rescued someone and earned some coins.", "You saved someone's life and earned some coins.", "You helped someone and earned some coins."],
  "police": ["You pulled over a speeder and earned wrote a ticket.", "You pulled over somone without their license and wrote a ticket.", "You pulled over someone without insurance and wrote a ticket.", "You pulled over someone who needs glasses but wasn't wearing them and wrote a ticket.", "You pulled over someone with unsecured hood cargo and wrote a ticket.", "You pulled over someone at night without their headlights on."],
  "doctor": ["You cured someone and earned some coins.", "You helped someone and earned some coins.", "You saved someone's life and earned some coins.", "You healed someone and earned some coins."],
  "ferry": ["You drove the ferry and sold some food. These passengers sure to pay a lot to eat!", "Someone paid you good money for some food. You drove them to the island.", "You delivered people to and from the island. They paid you good money for some food."],
  "trash": ["You recycled a lot of trash and sold it.", "You collected trash from the bottom of the ocean and helped save the enviroment!", "You removed trash from the ocean floor and sold it"],
  "mushroom": ["After collecting many mushrooms, you sold it to the mushroom lady.", "What a big haul! You sold many mushrooms to the mushroom lady.", "You sell many mushrooms to the mushroom lady."],
  "port": ["You steal some coin crates from the port and make big money.", "You steal some burger crates from the port and sell it to the bear.", "You steal some beef jerky crates and sell it to the bear.", "You steal some orange crates and sell it to the Vitamin C Enthusiast."],
  "debugjobid": ["Debug: Gave coins."]
}

vehicle_modifers = {
  "golfcart": 0.95,
  "car": 0.9,
  "sports": 0.8,
  "super": 0.7,
  "bike": 0.5,
  "debug": 0
}

food_hunger_refill = {
  "sausage": 1,
  "orange": 2,
  "burger": 5,
  "spaghetti": 100,
  "debug": 10000
}

item_type_from_id = {
  "sausage": "food",
  "orange": "food",
  "burger": "food",
  "spaghetti": "food",
  "golfcart": "vehicle",
  "car": "vehicle",
  "sports": "vehicle",
  "super": "vehicle",
  "bike": "vehicle",
  "bank": "upgrade",
  "food_meter": "upgrade",
  "shoes": "upgrade",
  "debug": "debug"
}

bank_levels = {
  0: {"price": 500, "capacity": 500, "name": "Tiny Bank Account", "description": "A tiny bank account that can hold up to 500 coins.", "interest": 0},
  1: {"price": 500, "capacity": 1000, "name": "Small Bank Account", "description": "A small bank account that can hold up to 1000 coins.", "interest": 0},
  2: {"price": 1000, "capacity": 2000, "name": "Medium Bank Account", "description": "A medium bank account that can hold up to 2000 coins.", "interest": 0},
  3: {"price": 3500, "capacity": 5000, "name": "Large Bank Account", "description": "A large bank account that can hold up to 5000 coins. Additionally, gains 0.1% interest each IRL day at 00:00 PST.", "interest": 0.1},
  4: {"price": 9000, "capacity": 10000, "name": "Huge Bank Account", "description": "A huge bank account that can hold up to 10000 coins. Additionally, gains 0.25% interest each IRL day at 00:00 PST.", "interest": 0.25},
  5: {"price": 20000, "capacity": 25000, "name": "Massive Bank Account", "description": "A massive bank account that can hold up to 25000 coins. Additionally, gains 0.5% interest each IRL day at 00:00 PST.", "interest": 0.5},
  6: {"price": 50000, "capacity": 50000, "name": "Gigantic Bank Account", "description": "A gigantic bank account that can hold up to 50000 coins. Additionally, gains 1% interest each IRL day at 00:00 PST.", "interest": 0.01},
  7: {"price": 100000, "capacity": 100000, "name": "Colossal Bank Account", "description": "A colossal bank account that can hold up to 100000 coins. Additionally, gains 2% interest each IRL day at 00:00 PST.", "interest": 0.02},
  8: {"price": 100000, "capacity": 100000, "name": "Colossal Bank Account", "description": "A colossal bank account that can hold up to 100000 coins. Additionally, gains 3.5% interest each IRL day at 00:00 PST.", "interest": 0.035},
  9: {"price": 200000, "capacity": 200000, "name": "Mega Bank Account", "description": "A mega bank account that can hold up to 200000 coins. Additionally, gains 5% interest each IRL day at 00:00 PST.", "interest": 0.05},
  10: {"price": 500000, "capacity": 500000, "name": "Ultra Bank Account", "description": "An ultra bank account that can hold up to 500000 coins. Additionally, gains 10% interest each IRL day at 00:00 PST.", "interest": 0.1},
  11: {"price": 1000000, "capacity": 1000000, "name": "Elite Only Bank Account", "description": "An elite only bank account that can hold up to 1000000 coins. Additionally, gains 20% interest each IRL day at 00:00 PST.", "interest": 0.2},
  12: {"price": 1000000, "capacity": 1000000, "name": "Waste of Money", "description": "With this much money, you can afford to waste some... right?", "interest": 0.2},
  13: {"price": 100000000, "capacity": 100000000000000, "name": "(Almost) Infinite Bank Account", "description": "Welp, you deserve this. If you can somehow make this much money, you'll be all set with this much interest!", "interest": 0.5},
  14: {"price": 100000000000, "capacity": 10000000000000000000000000000000000, "name": "WHAT", "description": "Well, I guess you deserve this insane interest rate. Good job on making this much money. Doubling your money every day is sure to get out of hand soon...", "interest": 1},
  15: {"price": 100000000000000000000000000000000000, "capacity": 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "description": "This is all your fault. The capacity number is really really long now, I don't know what more you want. Perhaps with this much money you can 10x your money every day? I don't even know how you managed this much money.", "interest": 9},
  16: {"price": 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, "name": "Humble Beginnings", "description": "1000x your money every day. Not only that, but your bank is truly infinite now. Maybe it's time to finally take a look at what you've accomplished. `|stats` to check your stats.", "interest": 999}
}

hunger_levels = {
  0: {"price": 0, "capacity": 6, "name": "Food Meter", "description": "A food meter that can hold up to 6 hunger points."},
  1: {"price": 500, "capacity": 7, "name": "Bigger Food Meter", "description": "A food meter that can hold up to 7 hunger points."},
  2: {"price": 1000, "capacity": 8, "name": "Even Bigger Food Meter", "description": "A food meter that can hold up to 8 hunger points."},
  3: {"price": 2000, "capacity": 9, "name": "Even Even Food Meter", "description": "A food meter that can hold up to 9 hunger points."},
  4: {"price": 3500, "capacity": 10, "name": "A Very Big Food Meter", "description": "A food meter that can hold up to 10 hunger points. Originally, this was supposed to be the biggest food meter."},
  5: {"price": 5000, "capacity": 11, "name": "A Very Very Big Food Meter", "description": "A food meter that can hold up to 11 hunger points. As it turns out, there are bigger food meters."},
  6: {"price": 7500, "capacity": 12, "name": "A Very Very Very Big Food Meter", "description": "A food meter that can hold up to 12 hunger points. Like this one."},
  7: {"price": 10000, "capacity": 13, "name": "The Big Food Meter", "description": "A food meter that can hold up to 13 hunger points. This one is pretty big."},
  8: {"price": 12000, "capacity": 14, "name": "The Bigger Food Meter", "description": "A food meter that can hold up to 14 hunger points. Who even needs this much food?"},
  9: {"price": 15000, "capacity": 15, "name": "The Biggest Food Meter", "description": "A food meter that can hold up to 15 hunger points."},
  10: {"price": 17500, "capacity": 16, "name": "Aboslute Maximum Food Meter", "description": "A food meter that can hold up to 16 hunger points."},
  11: {"price": 20000, "capacity": 17, "name": "The Food Meter", "description": "A food meter that can hold up to 17 hunger points."},
  12: {"price": 25000, "capacity": 18, "name": "Food Meter 18", "description": "A food meter that can hold up to 18 hunger points."},
  13: {"price": 35000, "capacity": 19, "name": "Food Meter 19 Plus", "description": "A food meter that can hold up to 19 hunger points."},
  14: {"price": 45000, "capacity": 20, "name": "Food Meter 20 Pro", "description": "A food meter that can hold up to 20 hunger points."},
  15: {"price": 60000, "capacity": 21, "name": "Food Meter 21 Pro Max", "description": "A food meter that can hold up to 21 hunger points."},
  16: {"price": 75000, "capacity": 22, "name": "Food Meter 22 Ultra", "description": "A food meter that can hold up to 22 hunger points."},
  17: {"price": 100000, "capacity": 23, "name": "Food Meter 23 Ultra Collector's Edition Fold 5G", "description": "A food meter that can hold up to 23 hunger points."},
  18: {"price": 110000, "capacity": 24, "name": "Foooooooooooooooooood Meter", "description": "A food meter that can hold up to 24 hunger points."},
  19: {"price": 120000, "capacity": 25, "name": "food meter", "description": "A food meter that can hold up to 25 hunger points."},
  20: {"price": 135000, "capacity": 26, "name": "FOOD METER!!!!!", "description": "A food meter that can hold up to 26 hunger points."},
  21: {"price": 150000, "capacity": 27, "name": "#FoodMeter", "description": "A food meter that can hold up to 27 hunger points."},
  22: {"price": 170000, "capacity": 28, "name": "food.meter", "description": "A food meter that can hold up to 28 hunger points."},
  23: {"price": 200000, "capacity": 29, "name": "@FOOD_METER", "description": "A food meter that can hold up to 29 hunger points."},
  24: {"price": 30000000, "capacity": 30, "name": "SACRIFICE", "description": "A food meter that can hold up to 30 hunger points. Why would you sacrifice this much money just for a marginally bigger food meter?"},
}

bot_dm_embed = discord.Embed(
  title="Sasbot invite link", description="Use this link to add Sasbot to your own Discord server! [Click here to invite me to your server!](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", color=0x00ff00
)

command_help = {
  'bal': 'Check how many coins you have.',
  'work': 'Work to earn coins.',
  'jobs': 'View all available jobs.',
  'shop': 'View all items in the shop. Optionally, you can view items from a specific shop category by running `|shop [name]`.',
  'buy': 'Buy an item from the shop. Useful for mass buying food. Run `|buy [item] [amount]`. Amount is optional.',
  'inv': 'View your inventory. Optionally, @ a user to view their inventory.',
  'eat': 'Eat food to refill your hunger bar. Equivalent to `|use [food]`.',
  'use': 'Use an item from your inventory. Run `|use [item]`.',
  'stats': 'View your stats. Optionally, @ a user to view their stats.',
  'help': 'View this help message.',
  'meme': 'View a random Sneaky Sasquatch meme. If you would like to submit a meme, DM <@773996537414942763>.',
  'debug': 'Debug command. Do not use. This command is only for debugging purposes.',
}