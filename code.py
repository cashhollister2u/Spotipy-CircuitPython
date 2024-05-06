# adafruit
import displayio
from adafruit_matrixportal.matrix import Matrix

# conventional libraries
from os import getenv
import time
import gc

# custom components
from views.view_stock import display_stock
from views.view_clock import display_clock
from components.clock import increment_time, JSON_clock 
from components.Spotipy_circuitpython.Authentication import refresh_access_token
from components.Spotipy_circuitpython.Player.player import spotify_player
from components.Spotipy_circuitpython.Player.player_parameters import currently_playing, pause_playback, resume_playback, set_playback_volume, skip_to_next, skip_to_previous

# env vaiables
IS_STOCK = getenv("IS_STOCK")
IS_CLOCK = getenv("IS_CLOCK")
IS_SPOTIFY = getenv("IS_SPOTIFY")
GLOBAL_ACCESS_TOKEN = refresh_access_token() # spotify

# Initialize the matrix
matrix = Matrix(bit_depth=4)

# Create a display object and rotating orientation
display = matrix.display
display.rotation = 180


# set up pixel control
bitmap = displayio.Bitmap(display.width, display.height, 256)  # 256 color palette
palette = displayio.Palette(256)

palette[0] = 0x000000  # Black, or 'off'
palette[1] = 0x4F0000  # Red
palette[2] = 0xA17272  # light red
palette[3] = 0x326132  # light green
palette[4] = 0x004F00  # Green
palette[5] = 0x00004F  # Blue 
palette[6] = 0x121111

def check_memory():
    free_memory = gc.mem_free()
    print("Free memory:", free_memory)
    return free_memory


# Keep the display running
while IS_CLOCK == 1:
    display_clock(display)
    increment_time(JSON_clock)
    time.sleep(1)
    
while IS_STOCK == 1:
    gc.collect()
    display_stock(bitmap, palette, display)
    time.sleep(1)

if IS_SPOTIFY == 1:
    print('spotify active')
    #spotify_player(currently_playing, GLOBAL_ACCESS_TOKEN)
    #if not GLOBAL_ACCESS_TOKEN:
    #    break

    #spotify_player(pause_playback, GLOBAL_ACCESS_TOKEN)

    #spotify_player(resume_playback, GLOBAL_ACCESS_TOKEN)

    #spotify_player(set_playback_volume, GLOBAL_ACCESS_TOKEN)
    
    #spotify_player(skip_to_next, GLOBAL_ACCESS_TOKEN)

    spotify_player(skip_to_previous, GLOBAL_ACCESS_TOKEN)

    time.sleep(5)
