import json
import datetime
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
      "inventory": [],
      "hunger": 6,
      "hunger_max": 6,
      "bank_balance": 0,
      "bank_lvl": 0,
      "earnings": 0,
      "shoe_lvl": 0,
      "early_tester": True,
      "date_joined": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open('data.json', 'w') as f:
      json.dump(users, f)
    return True
  return False

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
    json.dump(users, f)

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