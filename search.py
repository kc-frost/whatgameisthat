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

ACCESS_TOKEN = r_json['access_token']

headers = {
    'Client-ID': CLIENT_ID,
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

search_key = input("Enter game name: ")

important_fields = "id, name, game_type.type"
query = f'''
    fields {important_fields}, rating, storyline, summary;
    search "{search_key}";
    where game_type != (13, 5, 3) & version_parent = null & themes != (42) & rating != 0;
    limit 1;
'''

game_url = 'https://api.igdb.com/v4/games/'
response = requests.post(game_url, headers=headers, data=query)
g_json = response.json()

excluded_fields = ['name', 'game_type', 'rating']
try:
    for e in g_json:
        print(f"{e['name']}")
        for key, value in e.items():
            if key == 'rating':
                print(f"  {key}: {value:.2f}")
            if key not in excluded_fields:
                print(f"  {'IGDB ID' if key=='id' else key}: {value}")
except Exception as e:
    print(e)
