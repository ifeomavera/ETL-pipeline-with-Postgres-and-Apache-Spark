import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your credentials
client_id = 'da23dea1effe47aa9a166aae9f75a940'
client_secret = '372afc0e83154ed2976330775037b61e'
redirect_uri = 'http://localhost:8888/callback'

# Set up Spotify OAuth
scope = 'user-library-read playlist-read-private user-read-playback-state' 
sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, cache_path='.cache')

# Create a Spotipy client
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Print the list of available methods
methods = dir(sp)
#print(methods)

#To check the way the method behave 
for items in methods:
   print(help(items))
   print("-"* 20)


