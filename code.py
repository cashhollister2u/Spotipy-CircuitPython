# adafruit
from adafruit_matrixportal.matrix import Matrix

# conventional libraries
from os import getenv
import time

# custom components
from components.Spotipy_circuitpython.Authentication import refresh_access_token
from components.Spotipy_circuitpython.Player.player import spotify_player
from components.Spotipy_circuitpython.Player.player_parameters import currently_playing, pause_playback, resume_playback, set_playback_volume, skip_to_next, skip_to_previous

# env vaiables
IS_SPOTIFY = getenv("IS_SPOTIFY")
GLOBAL_ACCESS_TOKEN = refresh_access_token() # spotify


# if output then it will print in the terminal
while IS_SPOTIFY == 1: 
#if IS_SPOTIFY == 1:
    print('spotify active')
    spotify_player(currently_playing, GLOBAL_ACCESS_TOKEN)
    if not GLOBAL_ACCESS_TOKEN:
        break

    #spotify_player(pause_playback, GLOBAL_ACCESS_TOKEN)

    #spotify_player(resume_playback, GLOBAL_ACCESS_TOKEN)

    #spotify_player(set_playback_volume, GLOBAL_ACCESS_TOKEN)
    
    #spotify_player(skip_to_next, GLOBAL_ACCESS_TOKEN)

    #spotify_player(skip_to_previous, GLOBAL_ACCESS_TOKEN)

    time.sleep(5) #FOR THE WHILE LOOP OPTION

