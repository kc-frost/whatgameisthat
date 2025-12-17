import os
import requests
from dotenv import load_dotenv, dotenv_values

# variables
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TOKEN_URL = 'https://id.twitch.tv/oauth2/token'
GAME_URL = 'https://api.igdb.com/v4/games/'

IMPORTANT_FIELDS = "id, name, game_type.type, rating, summary"
EXCLUDED_FIELDS = ['name', 'game_type', 'rating']

# functions
def get_access_token() -> str:
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    response = requests.post(TOKEN_URL, json=data)
    try:
        response.raise_for_status
    except Exception as e:
        print (e)
    else:
        return response.json()['access_token']

def get_headers() -> dict:
    return {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {get_access_token()}'
    }

def return_game_info(game_name: str) -> any:
    query = f'''
        fields {IMPORTANT_FIELDS};
        search "{game_name}";
        where game_type != (13, 5, 3) & version_parent = null & themes != (42) & rating != 0;
        limit 1;
    '''
    response = requests.post(GAME_URL, headers=get_headers(), data=query)
    return response.json()

def main() -> None:
    # search for game
    search_key = input("Enter game name: ")
    game_info = return_game_info(search_key)

    try:
        no_games_returned: bool = len(game_info) == 0
        if (no_games_returned):
            raise Exception("No games were returned. Perhaps search under different terms?")
        else:
            for e in game_info:
                print(f"{e['name']}")
                for key, value in e.items():
                    if key == 'rating':
                        print(f"  {key}: {value:.2f}")
                    if key not in EXCLUDED_FIELDS:
                        print(f"  {'IGDB ID' if key=='id' else key}: {value}")
    except Exception as e:
        print(e)

if __name__ ==  '__main__':
    main()