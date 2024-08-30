import json
import datetime
from definitions import *

def ensure_user_in_json(user_id):
  with open('data.json', 'r') as f:
    users = json.load(f)

  in_users = False
  for user in users:
    if user_id == user['id']:
      in_users = True
      break

  if not in_users:
    users.append({
      "id": user_id,
      "coin_balance": 0,
      "work_job": "campground",
      "last_work": 0,
      "vehicles": [],
      "vehicle": "",
      "inventory": {},
      "hunger": 6,
      "hunger_max": 6,
      "bank_balance": 0,
      "bank_lvl": 0,
      "earnings": 0,
      "shoe_lvl": 0,
      "early_tester": True,
      "stats": {
        "total_coinsearned": 0,
        "total_works": 0,
        "works": {
          "campground": 0,
          "fishing": 0,
          "taxi": 0,
          "delivery": 0,
          "newspaper": 0,
          "paramedic": 0,
          "police": 0,
          "doctor": 0,
          "ferry": 0,
          "trash": 0,
          "mushroom": 0,
          "port": 0
        },
        "seconds_worked": 0,
        "max_coins": 0,
        "resets": 0,
        "bad_words": 0,
        "food_eaten": 0,
        "food_bought": 0
      },
      "settings": {
        "auto_buy": False,
        "detect_bad_words": False
      },
      "date_joined": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open('data.json', 'w') as f:
      json.dump(users, f, indent=2)
    return "added"
  # ensure user has all fields
  with open('data.json', 'r') as f:
    users = json.load(f)
    for user in users:
      if user_id == user['id']:
        try:
          # ensure user data version is up to date
          if 'data_version' not in user:
            user['data_version'] = current_user_data_version
          if 'coin_balance' not in user:
            user['coin_balance'] = 0
          if 'bank_balance' not in user:
            user['bank_balance'] = 0
          if 'bank_lvl' not in user:
            user['bank_lvl'] = 0
          if 'shoe_lvl' not in user:
            user['shoe_lvl'] = 0
          if 'early_tester' not in user:
            user['early_tester'] = True
          if 'date_joined' not in user:
            user['date_joined'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          if 'hunger' not in user:
            user['hunger'] = 6
          if 'hunger_max' not in user:
            user['hunger_max'] = 6
          if 'inventory' not in user:
            user['inventory'] = {}
          if 'vehicle' not in user:
            user['vehicle'] = ""
          if 'vehicles' not in user:
            user['vehicles'] = []
          if 'last_work' not in user:
            user['last_work'] = 0
          if 'work_job' not in user:
            user['work_job'] = "campground"
          if 'stats' not in user:
            print("Migrating user stats")
            user['stats'] = {
              "total_coinsearned": 0,
              "total_works": 0,
              "works": {
                "campground": 0,
                "fishing": 0,
                "taxi": 0,
                "delivery": 0,
                "newspaper": 0,
                "paramedic": 0,
                "police": 0,
                "doctor": 0,
                "ferry": 0,
                "trash": 0,
                "mushroom": 0,
                "port": 0
              },
              "seconds_worked": 0,
              "max_coins": 0,
              "resets": 0,
              "bad_words": 0,
              "food_eaten": 0,
              "food_bought": 0,
              "interest_earned": 0,
              "robbed": 0,
              "robbed_earned": 0,
              "robbed_lost": 0,
              "robbed_failed": 0,
              "debts": 0,
              "useless_stat": 0
            }
            print(user)
            print("User stats migrated")
          if 'settings' not in user:
            print("Migrating user settings")
            user['settings'] = {
              "auto_buy": False,
              "detect_bad_words": False
            }
            print("User settings migrated to default values")
          if 'earnings' in user:
            user['stats']['total_coinsearned'] = user['earnings']
            del user['earnings']
          if 'coin_balance' in user and 'stats' in user and 'total_coinsearned' in user['stats'] and user['coin_balance'] > 0 and user['stats']['total_coinsearned'] == 0:
            user['stats']['total_coinsearned'] += user['coin_balance']
          if user['data_version'] < current_user_data_version:
            print("Migrating user data")
            fields = ['coin_balance', 'work_job', 'last_work', 'vehicles', 'vehicle', 'inventory', 'hunger', 'hunger_max', 'bank_balance', 'bank_lvl', 'earnings', 'shoe_lvl', 'early_tester', 'stats', 'date_joined']
            stat_fields = ['total_coinsearned', 'total_works', 'works', 'seconds_worked', 'max_coins', 'resets', 'bad_words', 'food_eaten', 'food_bought', 'interest_earned', 'robbed', 'robbed_earned', 'robbed_lost', 'robbed_failed', 'debts', 'useless_stat']
            for field in fields:
              if field not in user:
                user[field] = 0
            for field in stat_fields:
              if field not in user['stats']:
                user['stats'][field] = 0
          if user['data_version'] < 4:
            print("Migrating inventory to new format")
            new_inventory = {}
            for item in user['inventory']:
              if item in new_inventory:
                new_inventory[item] += 1
              else:
                new_inventory[item] = 1
            user['inventory'] = new_inventory
            print(user['inventory'])
            user['data_version'] = 4
            print("Inventory migrated")
          user['data_version'] = current_user_data_version
        except Exception as e:
          print(e)
          return "corrupted"
    with open('data.json', 'w') as f:
      json.dump(users, f, indent=2)
  return "success"

def get_user_data(user_id):
  ensure_user_in_json(user_id)
  with open('data.json', 'r') as f:
    users = json.load(f)
    for user in users:
      if user_id == user['id']:
        return user
  return None

def save_user_data(user_id, user_data):
  with open('data.json', 'r') as f:
    users = json.load(f)
    for i in range(len(users)):
      if user_id == users[i]['id']:
        users[i] = user_data
        break
  with open('data.json', 'w') as f:
    json.dump(users, f, indent=2)

def get_job_data(job):
  with open('jobs.json', 'r') as f:
    jobs = json.load(f)
    for j in jobs:
      if job == j['id']:
        return j
      
def get_vehicle_data(vehicle):
  with open('vehicles.json', 'r') as f:
    vehicles = json.load(f)
    for v in vehicles:
      if vehicle == v['name']:
        return v
  return None

def get_all_users():
  users = []
  with open('data.json', 'r') as f:
    userjson = json.load(f)
  for user in userjson:
    users.append(user['id'])
  return users

def drop_user(user_id):
  with open('data.json', 'r') as f:
    users = json.load(f)
    for i in range(len(users)):
      if user_id == users[i]['id']:
        del users[i]
        break
  with open('data.json', 'w') as f:
    json.dump(users, f, indent=2)