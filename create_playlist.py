import sys
import spotipy
import spotipy.util as util
import fetch_songs
import os
import fetch_songs as fs
import svm_classifer as sc

def generate_playlist():
    #user = input("Enter your username: ")
    #user = "cv2f8pc6v4yqhx9qsgiiynji5"
    token = fs.get_token(user, scope = 'playlist-modify-private user-library-read')
    if token:
        sp = spotipy.Spotify(auth = token)
        split = int(input("0 for Work&Study, 1 for Happy&Sad: "))
        if os.path.exists("user.csv"):
            print("Deleting previous user's CSV file")
            os.remove("user.csv")
        playlist_dict = sc.predict(username = user, choice = split)
        allow_change = input("Type 0 if you want to add these playlist: ")
        if allow_change == '0':
            for playlist in playlist_dict:
                result = sp.user_playlist_create(user = user, name = playlist, public = False)
                master_list = playlist_dict[playlist]
                list_length = len(master_list)
                if list_length < 50:
                    sp.user_playlist_add_tracks(user = user, playlist_id = result['id'], tracks = master_list)
                else:
                    start = 0
                    end = 50
                    leftover = list_length
                    while True:
                        sp.user_playlist_add_tracks(user = user, playlist_id = result['id'], tracks = master_list[start:end])
                        if end == list_length : break
                        leftover -= 50
                        end += leftover if leftover < 50 else 50
                        start += 50
                print("Succesfully added the playlist to your account.")
        else:
            return 0
    else:
        print("Invalid Username")
        return 0
generate_playlist()
