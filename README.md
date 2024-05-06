# Spotipy-CircuitPython

A library used to authenticate and connect to your Spotify account using an Adafruit Matrix Portal

## Required:
- Spotify dev account and app

## Set-Up and Initial Authorization
1. Fill in settings.toml with CLIENT_ID and CLIENT_SECRET found on your Spotify Dev Account page
2. Ensure all available variables in the settings.toml file are also filled out with you information
3. Ensure "REFRESH_TOKEN" **IS** commented **out** in the settings.toml file
4. Run the code.py file on your Adafruit matrix portal with the dependencies included in the github repository
5. The terminal will output a url
6. Paste the url in your browser on a seconday device
7. Log into Spotify from the url you just opened
8. After logging in the url will direct you to a new webpage. (it may say "Failed to open page")
9. Copy the url of the page it redirected you to and paste it into the terminal
10.  It will output the access and refresh tokens
11.  Copy the Refresh token and paste it into the settings.toml file
12.  Make sure to comment **IN** the "REFRESH_TOKEN" variable in the settings.toml
13.  This will now notify the system that your account is Authorized and will no longer run that process
14.  The code will exit after this process
15.  Now re-run the code.py file it should now automatically connect and run the selected function.


## Commands

Main Function:
1. **spotify_player()**
- It accepts 2 parameters "Desired Action", "GLOBAL_ACCESS_TOKEN"

Desired Actions:
1. currently_playing
2. pause_playback
3. resume_playback
4. set_playback_volume
5. skip_to_next
6. skip_to_previous

## Examples
- Full code examples can be found in code.py
- Ensure the VOLUME variable is set in the settings.toml file when calling "set_volume_playback"

```
if IS_SPOTIFY == 1:
    spotify_player(set_playback_volume, GLOBAL_ACCESS_TOKEN)

```
- Get the song currently playing on Spotify account every 5 seconds
```
while IS_SPOTIFY == 1:
  print('spotify active')
  spotify_player(currently_playing, GLOBAL_ACCESS_TOKEN)
  if not GLOBAL_ACCESS_TOKEN:
    break
  
  time.sleep(5)

```
