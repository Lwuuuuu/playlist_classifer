import sys
import spotipy
import spotipy.util as util
import csv
def get_token(user, scope):
    token = util.prompt_for_user_token(username = user, scope = scope, client_id='1da08e2fb3994edebbf758e0fa0ab23b',     client_secret='98fe97db700b44f4ad0743b945e3084b',redirect_uri='http://localhost:8888/callback/')
    return token


def training_songs(sp, Training_Playlist):
    training_songs_id = set()
    #For all spotify playlist that is listed
    for playlist_info in Training_Playlist:
        index = 0
        while 1:
            results = sp.user_playlist_tracks('', playlist_id = playlist_info, limit = 100, offset = index)
            tracks = results['items']
            length = len(tracks)
            if length == 0:
                break
            index += length
            for track_id in tracks:
                #Adds the tracks ID to the set
                training_songs_id.add(track_id['track']['id'])
    return training_songs_id
def write_user(user_songs_id):
    with open('user.csv', 'a') as writeFile:
        writer = csv.writer(writeFile)
        for track in user_songs_id:
            writer.writerow(track)
def get_user_songs():
    try:
        with open('user.csv', 'r') as readFile:
            user_songs_id = []
            reader = csv.reader(readFile)
            csv_file = list(reader)
            for track_id in csv_file:
                user_songs_id.append(track_id)
    except:
        print("Entered the exception part where user data written to CSV.")
        token = get_token(user = "cv2f8pc6v4yqhx9qsgiiynji5", scope = 'user-library-read')
        sp = spotipy.Spotify(auth = token)
        user_songs_id = set()
        index = 0
        while 1:
            #Gets the users saved tracks
            results = sp.current_user_saved_tracks(limit=20, offset=index)
            user_songs = results['items']
            length = len(user_songs)
            #If all tracks from users saved tracks have been recorded
            if length == 0:
                break
            #Increase offset for next iteration
            index += length
            for track in user_songs:
                #adds the track ID to the list
                user_songs_id.add(track['track']['id'])
                #print(track['track']['name'])
        write_user(user_songs_id)
    return user_songs_id

