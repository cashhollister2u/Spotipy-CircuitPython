from os import getenv
from components.Spotipy_circuitpython.Authentication import get_user_authorization, extract_code_from_url, get_spotify_access_token, refresh_access_token

# grab env variables from settings.toml
REFRESH_TOKEN = getenv("REFRESH_TOKEN")

def spotify_player(player_callback_function, access_token):
    if not REFRESH_TOKEN:
        auth_url = get_user_authorization()
        auth_code = extract_code_from_url(auth_url)  # Safely extract the authorization code
        if auth_code:
            access_token = get_spotify_access_token(auth_code)
            if access_token:
                player_callback_function(access_token)
        else:
            print("Authorization failed. Please try again.")
    else:
        try:
            player_callback_function(access_token)
            print("Used Global Access")
        except:
            print('Failed to Use Global Access')            
            access_token = refresh_access_token()
            player_callback_function(access_token)