import sys
import spotipy
import spotipy.util as util

#WorkOut
Spotify_Beast_Mode = "https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP"
Spotify_Motivation_Mix = "https://open.spotify.com/playlist/37i9dQZF1DXdxcBWuJkbcy"
Spotify_Power_Workout = "https://open.spotify.com/playlist/37i9dQZF1DWUVpAXiEPK8P"
Spotify_Classic_Workout = "https://open.spotify.com/playlist/37i9dQZF1DWYNSm3Z3MxiM"
Spotify_Locked_In = "https://open.spotify.com/playlist/37i9dQZF1DWTl4y3vgJOXW"
Spotify_Hype = "https://open.spotify.com/playlist/37i9dQZF1DX4eRPd9frC1m"
Spotify_Raising_Bar = "https://open.spotify.com/playlist/37i9dQZF1DXdURFimg6Blm"
Spotify_Workout_Beats = "https://open.spotify.com/playlist/37i9dQZF1DWUSyphfcc6aL"
Training_Playlist = [Spotify_Beast_Mode, Spotify_Motivation_Mix, Spotify_Power_Workout, Spotify_Classic_Workout, Spotify_Locked_In, Spotify_Hype, Spotify_Raising_Bar,
Spotify_Workout_Beats]


#Study/Chill










#Upbeat/Fun




def get_token(user, scope):
    token = util.prompt_for_user_token(username = user, scope = scope, client_id='1da08e2fb3994edebbf758e0fa0ab23b',     client_secret='98fe97db700b44f4ad0743b945e3084b',redirect_uri='http://localhost:8888/callback/')
    return token


def training_songs(sp, playlist_info):
    training_songs_id = set()
    #Gets the Spotify playlist object
    #user = playlist_info[0]
    results = sp.user_playlist('', playlist_id = playlist_info)
    tracks = results['tracks']['items']
    for track_id in tracks:
        #Adds the tracks ID to the set
        training_songs_id.add(track_id['track']['id'])
    return training_songs_id
def get_user_songs(sp):
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
    return user_songs_id

