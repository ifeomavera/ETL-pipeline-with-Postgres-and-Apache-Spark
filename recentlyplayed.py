#import json
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy import create_engine

# Set your credentials
client_id = 'da23dea1effe47aa9a166aae9f75a940'
client_secret = '372afc0e83154ed2976330775037b61e'
redirect_uri = 'http://localhost:8888/callback'

# Set up Spotify OAuth
scope = 'user-read-recently-played' 
sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, cache_path='.cache')

# Create a Spotipy client
sp = spotipy.Spotify(auth_manager=sp_oauth)

#Creating the recent tracks log
historical_tracks_file = 'all_recent_tracks.csv'
#Checks if the file exists 
if os.path.exists(historical_tracks_file):
    historical_tracks_df = pd.read_csv(historical_tracks_file)
    tracks_ls = historical_tracks_df.to_dict('records')
else:
    tracks_ls = []

# Get current user's playlists
recent_tracks = sp.current_user_recently_played(limit=50)

# Print the track names, artist of each tracks and played times
""" for item in recent_tracks['items']:
    track = item['track']
    played_at = item['played_at']
    artist = track['artists'][0] 
    print(f"Track: {track['name']}")
    print(f"Played at: {played_at}")
    print(f"Artist: {artist['name']}")
    print("-------" * 10)  """

recent_tracks_ls = []

for item in recent_tracks['items']:
    track_name = item['track']['name']
    artist_name = item['track']['artists'][0]['name']
    played_at = item['played_at']
    
    recent_tracks_ls.append({
        'track_name': track_name,
        'artist_name': artist_name,
        'played_at': played_at
    })

tracks_ls.extend(recent_tracks_ls)
unique_tracks = {track['played_at']: track for track in tracks_ls}.values()

#print(tracks_ls)

df = pd.DataFrame(recent_tracks_ls)
track_df = pd.DataFrame(unique_tracks)
track_df.sort_values(by='played_at', inplace=True)

df.to_csv("recent_tracks.csv", index=False)
track_df.to_csv("all_recent_tracks.csv", index=False)
#Print the first 5 data
print(track_df.head())


username = 'ifeoma' 
password = 'postgre12' 
host = 'localhost' 
port = '5432'  
database_name = 'spotifydata' 

# Create a SQLAlchemy engine 
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}') 
# Load DataFrame into PostgreSQL table 
df.to_sql('recent_tracks', engine, if_exists='replace', index=False)
track_df.to_sql('all_recent_tracks', engine, if_exists='replace', index=False)

