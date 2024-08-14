help_output = """
## Sasbot Help
This is Adam The Great's interpretation of Sasbot. It contains an economy, and some fun commands.

**ECONOMY**
Make money using `|work`
Explore other jobs using `|jobs`
Buy useful items in the shop with `|shop`
Check how many coins you have with `|bal`
See your inventory with `|inv`

**FUN**
View a random Sneaky Sasquatch meme with `|meme` ||If you would like to submit a meme, run `|submitmeme`.||

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
    "description": "Fufilled exclusively by the spaghetti hotline. Heals the hunger bar by 6 points.",
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