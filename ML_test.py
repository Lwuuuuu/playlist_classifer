import spotipy
import spotipy.util as util
import sys
import csv
import os
import get_features as gf
from fetch_songs import get_token
token = get_token(user = '', scope = 'user-library-read')
#token = util.prompt_for_user_token(username = '', scope = 'user-library-read', client_id='1da08e2fb3994edebbf758e0fa0ab23b',        client_secret='98fe97db700b44f4ad0743b945e3084b',redirect_uri='http://localhost:8888/callback/')
sp = spotipy.Spotify(auth = token)
index = 0
#if os.path.exists('user.csv'): os.remove('user.csv')
csv_writer = open('features_happy_sad.csv', 'a')
writer = csv.writer(csv_writer)
while 1:
    #playlist = 'https://open.spotify.com/playlist/1SEuTassX0KSIl0fNX5oKz'
    #playlist = 'https://open.spotify.com/playlist/7vO1Nn5csaVPdodIDwKmoY'
    #playlist = 'https://open.spotify.com/playlist/37i9dQZF1DX4dyzvuaRJ0n'
    #playlist = 'https://open.spotify.com/playlist/37i9dQZF1DWXxauMBOQPxX'
    playlist = 'https://open.spotify.com/playlist/37i9dQZF1DZ06evO02uS96'
    #playlist = 'https://open.spotify.com/playlist/70Oa0hvBiMFwZDGC0UkS5s'
    results = sp.user_playlist_tracks('', playlist_id = sys.argv[1], limit = 100, offset = index)
    tracks = results['items']
    length = len(tracks)
    if length == 0:
        break
    index += length
    with open('user.csv', 'a') as f:
        for track_id in tracks:
            track_id = track_id['track']['id']
            if track_id is not None:
                #sample = gf.features(sp, track_id, 1)
                #sample.audio_features()
                #track = sample.return_features()
                #writer.writerow(track)
                #print(track)

                track_id = track_id + "\n"
                f.write(track_id)
#tracks = results['tracks']['items']
#training_songs_id = set()
#for track_id in tracks:
#    identifcation = track_id['track']['id']
#    print(identifcation)
csv_writer.close()
#    training_songs_id.add(identifcation)
