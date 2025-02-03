#import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy import create_engine

# Set your credentials
client_id = 'da23dea1effe47aa9a166aae9f75a940'
client_secret = '372afc0e83154ed2976330775037b61e'
redirect_uri = 'http://localhost:8888/callback'

# Set up Spotify OAuth
scope = 'user-top-read' 
sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, cache_path='.cache')

# Create a Spotipy client
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Get current user's playlists
top_artists = sp.current_user_top_artists(limit=50, time_range='medium_term')

artist_info_ls = []

for artist in top_artists['items']:
    artist_info = {
        'Artistname': artist['name'],
        'Genre' : artist['genres'] if artist['genres'] else ['Unknown Genre'],
        'FamousLevel': artist['popularity'],
        'Link': artist['external_urls']['spotify']
    }
    artist_info_ls.append(artist_info)

""" for info in artist_info_ls:
    print(f"Artist: {info['Artistname']}")
    print(f"Genres: {info['Genre']}")
    print(f"Popularity: {info['FamousLevel']}")
    print(f"Spotify URL: {info['Link']}")
    print("-------" * 10) """

all_artists = []
all_artists.extend(artist_info_ls)

df = pd.DataFrame(artist_info_ls)
df.to_csv('top_artists.csv', index=False)

all_df = pd.DataFrame(all_artists)
all_df.to_csv('all_artists.csv', index = False)

username = 'ifeoma' 
password = 'postgre12' 
host = 'localhost' 
port = '5432'  
database_name = 'spotifydata' 

# Create a SQLAlchemy engine 
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}') 
# Load DataFrame into PostgreSQL table 
df.to_sql('top_artists', engine, if_exists='replace', index=False)
all_df.to_sql('all_artists', engine, if_exists='replace', index=False)




