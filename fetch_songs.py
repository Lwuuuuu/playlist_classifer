import sys
import spotipy
import spotipy.util as util
import csv
import os
GLOBAL_SCOPE = 'user-library-modify playlist-modify-private user-library-read'
PATH = os.getcwd() + '/data/user.txt'
def get_token(user, scope):
    token = util.prompt_for_user_token(username = user, scope = scope, client_id='1da08e2fb3994edebbf758e0fa0ab23b',     client_secret='98fe97db700b44f4ad0743b945e3084b',redirect_uri='http://localhost:8888/callback/')
    return token

def training_songs(sp, Training_Playlist):
    training_songs_id = set()
    #For all spotify playlist that is listed
    for playlist_info in Training_Playlist:
        index = 0
        while 1:
            #Strip because need to get rid of the whitespaces in the playlist_info string
            results = sp.user_playlist_tracks('', playlist_id = playlist_info.strip(), limit = 100, offset = index)
            tracks = results['items']
            length = len(tracks)
            if length == 0:
                break
            index += length
            #Adds the tracks ID to the set
            [training_songs_id.add(track_id['track']['id']) for track_id in tracks]
    return training_songs_id
def get_user_songs(username):
    try:
        #If CSV file with user information exist
        with open(PATH, 'r') as f:
            #List containing all the track IDs of a user
            print("Text File Found")
            user_songs_id = []
            txt_file = f.readlines()
            [user_songs_id.append(track_id.rstrip("\n")) for track_id in txt_file]
    except:
        #If no user CSV File exist
        print("Loading in tracks into Text File")
        token = get_token(user = username, scope = GLOBAL_SCOPE)
        sp = spotipy.Spotify(auth = token)
        user_songs_id = set()
        index = 0
        while 1:
            #Gets the users saved tracks
            results = sp.current_user_saved_tracks(limit=20, offset=index)
            user_songs = results['items']
            length = len(user_songs)
            #If all tracks from users saved tracks have been recorded
            if length == 0: break
            #Increase offset for next iteration
            index += length
            #adds the track ID to the list
            [user_songs_id.add(track['track']['id']) for track in user_songs]
        with open(PATH, 'w') as writeFile:
            #Write IDs into user.csv
            for track in user_songs_id:
                track = track + "\n"
                writeFile.write(track)
    return user_songs_id
