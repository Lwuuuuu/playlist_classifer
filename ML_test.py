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


track = sp.track('43Wce6u3ukhWCxSyzywqJZ')
print(track['name'])
