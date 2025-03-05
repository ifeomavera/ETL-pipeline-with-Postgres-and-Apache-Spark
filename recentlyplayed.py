#import json
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy import create_engine
import schedule
import time
import subprocess

def job1():
    # Set your credentials
    client_id = 'da23dea1effe47aa9a166aae9f75a940'
    client_secret = '0ebadb5204dc46459d7b024b940e2e5f'
    redirect_uri = 'http://127.0.0.1:8888/callback'

    # Set up Spotify OAuth
    scope = 'user-read-recently-played'
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, cache_path='.cache')

    # Create a Spotipy client
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Creating the recent tracks log
    historical_tracks_file = 'all_recent_tracks.csv'
    # Checks if the file exists 
    if os.path.exists(historical_tracks_file):
        historical_tracks_df = pd.read_csv(historical_tracks_file)
        tracks_ls = historical_tracks_df.to_dict('records')
    else:
        tracks_ls = []

    # Get current user's playlists
    recent_tracks = sp.current_user_recently_played(limit=50)

    # Creating the recent tracks list
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

    df = pd.DataFrame(recent_tracks_ls)
    track_df = pd.DataFrame(unique_tracks)
    track_df.sort_values(by='played_at', inplace=True)

    df.to_csv("recent_tracks.csv", index=False)
    track_df.to_csv("all_recent_tracks.csv", index=False)
    # Print the first 5 data
    print(df.head())

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

    print("Pipeline executed!")

    # Run the other two scripts as subprocesses
   # subprocess.Popen(['python', 'top_tracks.py'])
    # subprocess.Popen(['python', 'topartist.py'])

# Schedule the job to run every 2 hours
#schedule.do(job1)
job1()
# Run the scheduler in a loop
# while True:
    # schedule.run_pending()
    # time.sleep(1)

