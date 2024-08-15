help_output = """
This is Adam The Great's interpretation of Sasbot. It contains an economy, and some fun commands.

**ECONOMY**
Make money using `|work`
Explore other jobs using `|jobs`
Buy useful items in the shop with `|shop`
Check how many coins you have with `|bal`
See your inventory with `|inv`

**FUN**
View a random Sneaky Sasquatch meme with `|meme` ||If you would like to submit a meme, DM <@773996537414942763>.||

This is just an early proof of conecpt.
-# Version 0.1.0
"""

welcome_output = f"""
Thank you for testing out this bot! It is currently a really early proof of concept. Many features are missing, and the bot is overall pretty buggy. 

To start making coins, run `|work`.
Keep an eye on your hunger bar! If it hits 0, there will be consequences. To fill it, run `|eat [food]`, where food is the name of the food you want to eat.
To see what is in your inventory (and see what food you have to eat), run `|inv`.

Take a look at `|help` for more information.
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
    "description": "Fufilled exclusively by the spaghetti hotline. Heals the entire hunger bar.",
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
  "shoes": "Shoes Upgrade"
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
  "port": ["You steal some coin crates from the port and make big money.", "You steal some burger crates from the port and sell it to the bear.", "You steal some beef jerky crates and sell it to the bear.", "You steal some orange crates and sell it to the Vitamin C Enthusiast."]
}

vehicle_modifers = {
  "golfcart": 0.95,
  "car": 0.9,
  "sports": 0.8,
  "super": 0.7,
  "bike": 0.5
}

food_hunger_refill = {
  "sausage": 1,
  "orange": 2,
  "burger": 5,
  "spaghetti": 10
}

item_type_from_id = {
  "sausage": "food",
  "orange": "food",
  "burger": "food",
  "spaghetti": "food"
}