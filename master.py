import sys
import spotipy
import spotipy.util as util
from fetch_songs import get_token
import os
import csv
import fetch_songs as fs
import svm_classifer as sc
GLOBAL_SCOPE = 'user-library-modify playlist-modify-private user-library-read'
PATH = os.getcwd() + '/data/user.txt'
def add_tracks(sp, master_list, result = None):
    list_length = len(master_list)
    if list_length < 50:
        #If the number of songs to add is less than 50, can do it in one call
        if result is not None:
            #If adding tracks to a created playlist
            sp.user_playlist_add_tracks(user = user, playlist_id = result['id'], tracks = master_list)
        else:
            #If adding tracks to the song library
            sp.current_user_saved_tracks_add(master_list)
    else:
        start = 0
        end = 50
        leftover = list_length
        #Have to make multiple calls if the added tracks is over 50 as 50 is the limit per call
        while True:
            if result is not None:
                sp.user_playlist_add_tracks(user = user, playlist_id = result['id'], tracks = master_list[start:end])
            else:
                sp.current_user_saved_tracks_add(master_list)
            if end == list_length : break
            leftover -= 50
            end += leftover if leftover < 50 else 50
            start += 50
    print("Succesfully added the playlist to your account.")

def generate_playlist(user, split):
    token = fs.get_token(user, scope = GLOBAL_SCOPE)
    if token:
        sp = spotipy.Spotify(auth = token)
        if os.path.exists(PATH):
            #Re-load user.csv file with new user information
            os.remove(PATH)
            print("Deleting previous user's CSV file")
        #Playlist_dict will have either Workout/Study or Happy/Sad accompied with their list of track IDs
        playlist_dict = sc.predict(username = user, choice = split)
        allow_change = input("Type 0 if you want to add these playlist: ")
        if allow_change == '0':
            for playlist in playlist_dict:
                #Creating the mood playlist in user's Spotify account
                result = sp.user_playlist_create(user = user, name = playlist, public = False)
                master_list = playlist_dict[playlist]
                add_tracks(sp, master_list, result)
        else:
            return 0
    else:
        print("Invalid Username")
        return 0
    os.remove(PATH)
def classify_Playlist(URL, username, choice = 0):
    token = get_token(user = username, scope = GLOBAL_SCOPE)
    if token:
        sp = spotipy.Spotify(auth = token)
        index = 0
        while 1:
            #Gets the tracks for the specified URL
            results = sp.user_playlist_tracks(user = username, playlist_id = URL, limit = 100, offset = index)
            tracks = results['items']
            length = len(tracks)
            if length == 0: break
            index += length
            #Writes the track IDs to user.csv
            with open(PATH, 'w') as f:
                for track_id in tracks:
                    track_id = track_id['track']['id']
                    track_id = track_id + "\n"
                    f.write(track_id)
        #This will classify each track into one of the two groups stored in a dict
        mood_dict = sc.predict(username, split)
        moods = []
        #Gets a list of the dict key values
        [moods.append(x) for x in mood_dict]
        Add = input("Type 1 if you want to add these songs to your song library: ")
        if Add == '1':
            print("Type 0 for {0}, Type 1 for {1}, Type 2 for Both: ".format(moods[0], moods[1]))
            decision = input()
            if decision == '0': track_list = mood_dict[moods[0]]
            if decision == '1': track_list = mood_dict[moods[1]]
            if decision == '2': track_list = mood_dict[moods[0]] + mood_dict[moods[1]]
            else: return 0
            #Do not add a song to song library is that song is already there
            current_songs = fs.get_user_songs(username)
            for track in track_list:
                if track in current_songs:
                    track_name = sp.track(track)['name']
                    print(track_name, "already found in song library.")
                    track_list.remove(track)
            add_tracks(sp, track_list)
            print("Tracks have been succesfully added to your song library")
        os.remove(PATH)
    else:
        print("Invalid Username")
        return 0
if __name__ == '__main__':
    #user = "cv2f8pc6v4yqhx9qsgiiynji5"
    username = input("Enter your username: ")
    Input = input("Type 0 to Classify a Playlist, Type 1 to Classify your Songs: ")
    split = int(input("0 for Work&Study, 1 for Happy&Sad: "))
    if Input == '0':
        #Playlist Classifcation
        URL = input("Paste the Playlist URL: ")
        classify_Playlist(URL, username, split)
    if Input == '1':
        #Classify user's song library
        generate_playlist(username, split)
