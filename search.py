import os
import requests
from dotenv import load_dotenv, dotenv_values

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

url = 'https://id.twitch.tv/oauth2/token'
data = {
    'client_id':CLIENT_ID,
    'client_secret':CLIENT_SECRET,
    'grant_type':'client_credentials'
}

response = requests.post(url, json=data)
r_json = response.json()

# print(r_json)

ACCESS_TOKEN = r_json['access_token']

headers = {
    'Client-ID': CLIENT_ID,
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

# where name = "Persona"* & game_type = 0 & expanded_games != null;
query = '''
    fields id, name, game_type.type, dlcs, expansions, expanded_games, parent_game, version_parent, game_status.status;
    search "Persona Reload";
    where name = "Persona"* & game_type != (1, 13, 5, 3) & version_parent = null;
    limit 100;
'''

game_url = 'https://api.igdb.com/v4/games/'
r = requests.post(game_url, headers=headers, data=query)
g_json = r.json()
count = 0
try:
    for e in g_json:
        print(f"[{count}] id: {e['id']}")
        for key, value in e.items():
            if key != 'id':
                print(f"  {key}: {value}")
        count += 1
except Exception as e:
    print(e)
