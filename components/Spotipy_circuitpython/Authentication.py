from os import getenv
from components.network_connect import requests

# grab env variables from settings.toml
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
REFRESH_TOKEN = getenv("REFRESH_TOKEN")


# custom urlencode funct
def urlencode(query): 
    def escape(s):
        s = str(s)
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-"
        return ''.join([c if c in safe_chars else '%{:02X}'.format(ord(c)) for c in s])

    return '&'.join([f"{escape(k)}={escape(v)}" for k, v in query.items()])

# should only need to be done once 
def get_user_authorization():
    """Directs the user to the Spotify login page for authorization."""
    query_params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8080/',
        'scope': 'user-read-currently-playing user-modify-playback-state', #look at spotify api documentaion for different scopes
    }
    url = f"https://accounts.spotify.com/authorize?{urlencode(query_params)}"
    print(url)
    return input("Paste the URL you were redirected to: ")

def get_spotify_access_token(code):
    """Exchange the authorization code for an access token."""
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:8080/',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("\nToken retrieved successfully!")
        print('\nPASTE REFRESH TOKEN INTO settings.toml as "REFRESH_TOKEN =" ')
        print(f"\naccess:{response.json()['access_token']}")
        print(f"\nrefresh:{response.json()['refresh_token']}")
        
        
        return response.json()['access_token']
    
    else:
        print("Failed to retrieve access token:", response.json())
        return None

def refresh_access_token():
    """Use the refresh token to obtain a new access token."""
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        new_tokens = response.json()
        print('refreshed token')
        return new_tokens['access_token']
    else:
        print("Failed to refresh access token:", response.json())
        return None

def extract_code_from_url(url):
    """Extracts the authorization code from a given URL or indicates failure."""
    try:
        return url.split("code=")[1].split("&")[0]
    except IndexError:
        print("Failed to extract the authorization code. Please make sure you've entered the correct URL.")
        return None
    
