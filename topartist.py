#import json
import os 
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy import create_engine
import schedule
import time

def job3():
    # Set your credentials
    client_id = 'da23dea1effe47aa9a166aae9f75a940'
    client_secret = '0ebadb5204dc46459d7b024b940e2e5f'
    redirect_uri = 'http://127.0.0.1:8888/callback'

    # Set up Spotify OAuth
    scope = 'user-top-read' 
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, cache_path='.cache')

    # Create a Spotipy client
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Get current user's playlists
    historical_artists_file = 'all_top_artists.csv'
    if os.path.exists(historical_artists_file):
        historical_artists_df = pd.read_csv(historical_artists_file)
        all_artists = historical_artists_df.to_dict('records')
    else:
        all_artists = []

    # Get current user's top artists
    top_artists = sp.current_user_top_artists(limit=50, time_range='medium_term')

    # Create a list to hold new artist information
    artist_info_ls = []

    for artist in top_artists['items']:
        artist_info = {
            'Artistname': artist['name'],
            'Genre': artist['genres'] if artist['genres'] else ['Unknown Genre'],
            'FamousLevel': artist['popularity'],
            'Link': artist['external_urls']['spotify']
        }
        artist_info_ls.append(artist_info)

    all_artists.extend(artist_info_ls)

    unique_artists = {artist['Artistname']: artist for artist in all_artists}.values()

    df = pd.DataFrame(artist_info_ls)
    all_df = pd.DataFrame(unique_artists)
    #all_df.sort_values(by='Artistname', inplace=True)

    df.to_csv('top_artists.csv', index=False)
    all_df.to_csv('all_top_artists.csv', index = False)

    username = 'ifeoma' 
    password = 'postgre12' 
    host = 'localhost' 
    port = '5432'  
    database_name = 'spotifydata' 

    # Create a SQLAlchemy engine 
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}') 
    # Load DataFrame into PostgreSQL table 
    df.to_sql('top_artists', engine, if_exists='replace', index=False)
    all_df.to_sql('all_top_artists', engine, if_exists='replace', index=False)

    print("Top Artists Pipeline executed!")

# Schedule the job to run every hour
# schedule.every(4).hours.do(job3)
job3()
# Run the scheduler in a loop
# while True:
    # schedule.run_pending()
    # time.sleep(1)






