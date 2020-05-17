# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 18:58:16 2020

@author: penko
"""

import time
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd
import numpy as np

    
##############
#
# Transform track data
#
##############

def streamingHistoryData():
    # Open files, concatenate
    # Number of files may vary depending on the size of the data Spotify sends
    with open(r'.\StreamingHistory0.json', encoding='utf-8') as f0:
        with open(r'.\StreamingHistory1.json', encoding='utf-8') as f1:
            tjson = json.load(f0) + json.load(f1)
    
    # DataFrame for tracks. Doesn't have id's yet for other queries
    shd = pd.DataFrame( [ {
            "trackName": t['trackName'],
            "artistName": t['artistName'],
            "endTime": t['endTime'],
            "msPlayed": t['msPlayed']
        } for t in tjson ] )
    
    return shd

def playlistData():
    with open(r'.\Playlist1.json', encoding='utf-8') as p1:
        pjson = json.load(p1)
        
    pldf = pd.DataFrame( [ {
            "playlistName": pl['name'],
            "trackName": track['track']['trackName'],
            "artistName": track['track']['artistName'],
            "albumName": track['track']['albumName']
            #"localTrack": True if track['localTrack'] != None else False,
        } for pl in pjson['playlists'] for track in pl['items'] if (track['localTrack'] == None and pl['name'] != 'Old School Chillin')] )
    
    return pldf


def getTrackIDs(df):
    tempdf = df.copy()
    # internal function to see if the track is the same as the search
    def songmatch(searchresult, tName, aName):
        if len(searchresult['tracks']['items']) == 0:
            return -1
        for i, song in enumerate(searchresult['tracks']['items']):
            # find correct track title
            if song['name'] != tName:
                continue
            # find correct artist
            if aName not in [a['name'] for a in song['artists']]:
                continue
            # found match
            return i
        return -1
    
    
    
    cache = {}
    newdf = pd.DataFrame({'trackId': [],
                         'artistId': [],
                         #'artistName': [],
                         'albumId': [],
                         'albumName': [],
                         'image640': [],
                         'image300': [],
                         'image64': [],
                         'trackPopularity': [],
                         'previewUrl': []})
    
    for i, t in enumerate(tempdf.itertuples()):
        if (i != 0 and i%100 == 0):
            print('sleeping with ' + str(i) + "/" + str(len(tempdf['trackName'])) + ' (' + str(round(100*i/len(tempdf['trackName']), 2)) + '%) completed...')
            time.sleep(1)
            print("resuming...")
        row = t._asdict()
        
        if (row['trackName'], row['artistName']) in cache:
            newdf = newdf.append(pd.DataFrame({'trackId': cache[(row['trackName'], row['artistName'])]['trackId'],
                              'artistId': cache[(row['trackName'], row['artistName'])]['artistId'],
                              #'artistName': cache[(row['trackName'], row['artistName'])]['artistName'],
                              'albumId': cache[(row['trackName'], row['artistName'])]['albumId'],
                              'albumName': cache[(row['trackName'], row['artistName'])]['albumName'],
                              'image640': cache[(row['trackName'], row['artistName'])]['image640'],
                              'image300': cache[(row['trackName'], row['artistName'])]['image300'],
                              'image64': cache[(row['trackName'], row['artistName'])]['image64'],
                              'trackPopularity': cache[(row['trackName'], row['artistName'])]['trackPopularity'],
                              'previewUrl': cache[(row['trackName'], row['artistName'])]['previewUrl']}, index = [i]))
        else:
            qry = 'track:"{}" artist:"{}"'.format(row['trackName'].replace("'",""), row['artistName'].replace("'",""))
            trcall = sp.search(q=qry, limit=10, type="track")
            # If we didn't get any results, or artist/song name don't match, null for ID
            smatch = songmatch(trcall, row['trackName'], row['artistName'])
            
            if smatch == -1:
                newdf = newdf.append(pd.DataFrame({'trackId': None,
                    'artistId': None,
                    #'artistName': artistname,
                    'albumId': None,
                    'albumName': None,
                    'image640': None,
                    'image300': None,
                    'image64': None,
                    'trackPopularity': None,
                    'previewUrl': None}, index = [i]))
                cache[(row['trackName'], row['artistName'])] = {
                    'trackId': None,
                    'artistId': None,
                    #'artistName': None,
                    'albumId': None,
                    'albumName': None,
                    'image640': None,
                    'image300': None,
                    'image64': None,
                    'trackPopularity': None,
                    'previewUrl': None
                }
            else:
                artistid, artistname = "", ""
                for a in trcall['tracks']['items'][smatch]['artists']:
                    if a['name'] == row['artistName']:
                        artistid = a['id']
                        artistname = a['name']
                img640, img300, img64 = "", "", ""
                for image in trcall['tracks']['items'][smatch]['album']['images']:
                    if image['height'] == 640 or image['width'] == 640:
                        img640 = image['url']
                    elif image['height'] == 300 or image['width'] == 300:
                        img300 = image['url']
                    elif image['height'] == 64 or image['width'] == 64:
                        img64 = image['url']
                # Add to new df
                newdf = newdf.append(pd.DataFrame({'trackId': trcall['tracks']['items'][smatch]['id'],
                              'artistId': artistid,
                              #'artistName': artistname,
                              'albumId': trcall['tracks']['items'][smatch]['album']['id'],
                              'albumName': trcall['tracks']['items'][smatch]['album']['name'],
                              'image640': img640,
                              'image300': img300,
                              'image64': img64,
                              'trackPopularity': trcall['tracks']['items'][smatch]['popularity'],
                              'previewUrl': trcall['tracks']['items'][smatch]['preview_url'] if trcall['tracks']['items'][smatch]['preview_url'] is not None else None}, index = [i]))
                # Add to cache
                cache[(row['trackName'],row['artistName'])] = {'trackId': trcall['tracks']['items'][smatch]['id'],
                              'artistId': artistid,
                              #'artistName': artistname,
                              'albumId': trcall['tracks']['items'][smatch]['album']['id'],
                              'albumName': trcall['tracks']['items'][smatch]['album']['name'],
                              'image640': img640,
                              'image300': img300,
                              'image64': img64,
                              'trackPopularity': trcall['tracks']['items'][smatch]['popularity'],
                              'previewUrl': trcall['tracks']['items'][smatch]['preview_url'] if trcall['tracks']['items'][smatch]['preview_url'] is not None else None}
    
    tempdf[['trackId','artistId','albumId','albumName','image640','image300','image64','trackPopularity','previewUrl']] = newdf
    
    return tempdf



def getAudioFeatures(df):
    # Remove NA's
    tempdf = df[df['trackId'].notna()].reset_index(drop = True)
    
    features = ['danceability','energy','key','loudness',
                'mode','speechiness','acousticness','instrumentalness',
                'liveness','valence','tempo','duration_ms']
    
    # <cite>
    # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    # <\cite>
            
    tempdf_unique = list(set(tempdf['trackId']))
    tempdf_chunks = list(chunks(tempdf_unique, 50))
    
    tempdf[features] = pd.DataFrame(np.transpose([np.zeros_like(tempdf['trackId']) for _ in range(len(features))]))
    
    for i, chunk in enumerate(tempdf_chunks):
        print("Starting chunk {}/{}".format(i+1, len(tempdf_chunks)))
        # Call API for chunk
        ch_ret = sp.audio_features(chunk)
        
        # Extract data
        for tr in ch_ret:
            tempdf.loc[tempdf['trackId'] == tr['id'], features] = [
                tr['danceability'],
                tr['energy'],
                tr['key'],
                tr['loudness'],
                tr['mode'],
                tr['speechiness'],
                tr['acousticness'],
                tr['instrumentalness'],
                tr['liveness'],
                tr['valence'],
                tr['tempo'],
                tr['duration_ms']
            ]
    return tempdf

# Example:
'''
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

tracks = streamingHistoryData()
tracks = getTrackIDs(tracks)
tracks = getAudioFeatures(tracks)
tracks = tracks.replace("’","'",regex = True)
tracks = tracks.replace('“','"',regex = True)
tracks = tracks.replace('”','"',regex = True)

#tracks.to_pickle(r'.\tracks.pkl')
#tracks.to_csv(r'.\tracks.csv')

pldat = playlistData()
pldat = getTrackIDs(pldat)
pldat = getAudioFeatures(pldat)
pldat = pdf.replace("’","'",regex = True)
pldat = pdf.replace('“','"',regex = True)
pldat = pdf.replace('”','"',regex = True)

#pldat.to_pickle(r'.\pldat.pkl')
#pldat.to_csv(r'.\pldat.csv')

'''