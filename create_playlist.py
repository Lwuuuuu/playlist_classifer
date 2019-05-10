import sys
import spotipy
import spotipy.util as util
import fetch_songs

def create_playlist(sp, user_id):
    #user_id = sp.current_user()['id']
    print(user_id)
    result = sp.user_playlist_create(user = user_id, name = "STUDYING", public = False)
def add_tracks(sp, user, master_list):
    #sp.user_playlist_add_tracks(master_list)
    master_list = list(master_list)
    print(master_list)
    Playlist = sp.current_user_playlists()
    Work = Playlist['items'][0]['id']
    sp.user_playlist_add_tracks(user = user, playlist_id = Work, tracks = master_list[:100])

def run():
    user = "cv2f8pc6v4yqhx9qsgiiynji5"
    token = util.prompt_for_user_token(username = user, scope = 'playlist-modify-private', client_id='1da08e2fb3994edebbf758e0fa0ab23b',
    client_secret='98fe97db700b44f4ad0743b945e3084b',redirect_uri='http://localhost:8888/callback/')
    if token:
        sp = spotipy.Spotify(auth=token)
        #master_list, user_list = run()
        create_playlist(sp, user) 
run()
