from os import getenv
from components.network_connect import requests

VOLUME = getenv("VOLUME")

def currently_playing(access_token):
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        track_name = data['item']['name']
        artist_name = data['item']['artists'][0]['name']
        print(f"\nCurrently playing: {track_name} by {artist_name}")
    elif response.status_code == 403:
        print("Spotify Skip failed: User is not a premium user (required for this operation).")
    else:
        raise Exception(f"Failed to retrieve data, status code: {response.status_code}")

def pause_playback(access_token):
    url = 'https://api.spotify.com/v1/me/player/pause'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Length': '0'
        }

    response = requests.put(url, headers=headers)
    if response.status_code == 204:  # Success with no content returned
        print(f"\nPaused Spotify")
    elif response.status_code == 403:
        print("Pause failed: User is not a premium user (required for this operation).")
    elif response.status_code == 404:
        print("Pause failed: No active device found or track currently playing.")
    else:
        raise Exception(f"Failed to pause, status code: {response.status_code}")
    
def resume_playback(access_token):
    url = 'https://api.spotify.com/v1/me/player/play'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Length': '0'
        }

    response = requests.put(url, headers=headers)
    if response.status_code == 204:  # Success with no content returned
        print(f"\nResumed Spotify")
    elif response.status_code == 403:
        print("Resume failed: User is not a premium user (required for this operation).")
    elif response.status_code == 404:
        print("Resume failed: No active device found or track paused.")
    else:
        raise Exception(f"Failed to Resume, status code: {response.status_code}")

def set_playback_volume(access_token):
    url = f'https://api.spotify.com/v1/me/player/volume?volume_percent={VOLUME}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Length': '0'
        }

    response = requests.put(url, headers=headers)
    if response.status_code == 204:  # Success with no content returned
        print(f"\nSpotify Volume Set")
    elif response.status_code == 403:
        print("Set Volume failed: User is not a premium user (required for this operation).")
    elif response.status_code == 404:
        print("Set Volume failed: No active device found.")
    else:
        raise Exception(f"Set Volume failed, status code: {response.status_code}")

def skip_to_next(access_token):
    url = 'https://api.spotify.com/v1/me/player/next'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Length': '0'
        }

    response = requests.post(url, headers=headers)
    if response.status_code == 204:  # Success with no content returned
        print(f"\nSpotify Skip")
    elif response.status_code == 403:
        print("Spotify Skip failed: User is not a premium user (required for this operation).")
    elif response.status_code == 404:
        print("Spotify Skip failed: No active device found.")
    else:
        raise Exception(f"Spotify Skip failed, status code: {response.status_code}")

def skip_to_previous(access_token):
    url = 'https://api.spotify.com/v1/me/player/previous'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Length': '0'
        }

    response = requests.post(url, headers=headers)
    if response.status_code == 204:  # Success with no content returned
        print(f"\nSpotify Previous")
    elif response.status_code == 403:
        print("Spotify Previous failed: User is not a premium user (required for this operation).")
    elif response.status_code == 404:
        print("Spotify Previous failed: No active device found.")
    else:
        raise Exception(f"Spotify Previous failed, status code: {response.status_code}")