import spotipy
import spotipy.util as util
import sys
token = util.prompt_for_user_token(username = '', scope = 'user-library-read')
#token = util.prompt_for_user_token(username = '', scope = 'user-library-read', client_id='1da08e2fb3994edebbf758e0fa0ab23b',        client_secret='98fe97db700b44f4ad0743b945e3084b',redirect_uri='http://localhost:8888/callback/')
sp = spotipy.Spotify(auth = token)
index = 0
while 1:
    #playlist = 'https://open.spotify.com/playlist/1SEuTassX0KSIl0fNX5oKz'
    playlist = 'https://open.spotify.com/playlist/7vO1Nn5csaVPdodIDwKmoY'
    #playlist = 'https://open.spotify.com/playlist/70Oa0hvBiMFwZDGC0UkS5s'
    results = sp.user_playlist_tracks('', playlist_id = playlist, limit = 100, offset = index)
    tracks = results['items']
    length = len(tracks)
    if length == 0:
        break
    index += length
    for track_id in tracks:
        print(track_id['track']['id'])
#tracks = results['tracks']['items']
#training_songs_id = set()
#for track_id in tracks:
#    identifcation = track_id['track']['id']
#    print(identifcation)
#    training_songs_id.add(identifcation)
