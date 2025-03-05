#import json
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy import create_engine
import schedule
import time

def job2():
    # Set your credentials
    client_id = 'da23dea1effe47aa9a166aae9f75a940'
    client_secret = '0ebadb5204dc46459d7b024b940e2e5f'
    redirect_uri = 'http://127.0.0.1:8888/callback'

    # Set up Spotify OAuth
    scope = 'user-top-read' 
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, cache_path='.cache')

    # Create a Spotipy client
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Creating the recent tracks log
    historical_tracks_file = 'all_top_tracks.csv'
    # Checks if the file exists 
    if os.path.exists(historical_tracks_file):
        historical_tracks_df = pd.read_csv(historical_tracks_file)
        tracks_ls = historical_tracks_df.to_dict('records')
    else:
        tracks_ls = []

    # Get current user's top tracks
    top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')
    top_tracks_ls = []

    for item in top_tracks['items']:
        track_name = item['name']
        artist_name = item['artists'][0]['name']
        duration = item['duration_ms']
        popularity = item['popularity']
        preview_url = item['preview_url']
        uri = item['uri']
        
        top_tracks_ls.append({
            'id': uri,
            'track_name': track_name,
            'artist_name': artist_name,
            'duration': duration,
            'popularity': popularity,
            'link': preview_url,
        })

    tracks_ls.extend(top_tracks_ls)
    unique_tracks = {track['id']: track for track in tracks_ls}.values()

    df = pd.DataFrame(top_tracks_ls)
    track_df = pd.DataFrame(unique_tracks)

    # Sort the historical data by 'track_name'
    track_df.sort_values(by='track_name', inplace=True)

    df.to_csv("top_tracks.csv", index=False)
    track_df.to_csv("all_top_tracks.csv", index=False)
    # Print the first 5 data
    print(track_df.head())

    username = 'ifeoma'
    password = 'postgre12'
    host = 'localhost'
    port = '5432'
    database_name = 'spotifydata'

    # Create a SQLAlchemy engine
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}')
    # Load DataFrame into PostgreSQL table
    df.to_sql('top_tracks', engine, if_exists='replace', index=False)
    track_df.to_sql('all_top_tracks', engine, if_exists='replace', index=False)

    print("Top Tracks Pipeline executed!")

# Schedule the job to run every hour
#schedule.every(3).hours.do(job2)
job2()
# Run the scheduler in a loop
#while True:
    #schedule.run_pending()
    #time.sleep(1)


