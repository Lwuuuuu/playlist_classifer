import sys
import spotipy
import spotipy.util as util
import os
import fetch_songs as fs
import random
import numpy as np
import csv
GLOBAL_SCOPE = 'user-library-modify playlist-modify-private user-library-read'
feature_types = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
'valence', 'tempo']
HAPPY_PATH = os.getcwd() + '/data/Happy.txt'
SAD_PATH = os.getcwd() + '/data/Sad.txt'
user_file = os.getcwd() + '/data/user.csv'
HAP_SAD_FEATURES = os.getcwd() + '/data/features_happy_sad.csv'
class Spotify():
    def __init__(self, username):
        self.username = username
        self.token = self.get_token(GLOBAL_SCOPE)
        self.sp = spotipy.Spotify(auth = self.token)
        self.user_tracks_id = set()
        self.user_audio_features = None
        self.training_tracks_id = []
        self.training_audio_features = None
    def get_token(self, scope):
        self.token = util.prompt_for_user_token(username = self.username, scope = scope, client_id='1da08e2fb3994edebbf758e0fa0ab23b',
        client_secret='98fe97db700b44f4ad0743b945e3084b',redirect_uri='http://localhost:8888/callback/')
    def load_user_tracks(self):
        index = 0
        while 1:
            results = self.sp.current_user_saved_tracks(limit=20, offset=index)
            user_songs = results['items']
            length = len(user_songs)
            #If all tracks from users saved tracks have been recorded
            if length == 0: break
            index += length
            #adds the track ID to the set
            [self.user_tracks_id.add(track['track']['id']) for track in user_songs]
    def load_training_tracks(self, Training_Playlist):
        mood_playlist = set()
        #For all spotify playlist that is listed
        for playlist_info in Training_Playlist:
            index = 0
            while 1:
                #Strip because need to get rid of the whitespaces in the playlist_info string
                results = self.sp.user_playlist_tracks('', playlist_id = playlist_info.strip(), limit = 100, offset = index)
                tracks = results['items']
                length = len(tracks)
                if length == 0:
                    break
                index += length
                #Adds the tracks ID to the set
                [mood_playlist.add(track_id['track']['id']) for track_id in tracks]
    def load_features(self, id_list, audio_ft, fi):
        id_length = len(id_list)
        audio_ft = np.zeros([id_length, len(feature_types)], dtype = np.float32)
        start = 0
        if id_length <= 50:
            iter = id_length
        else:
            iter = 50
        f = open(fi, 'a')
        writer = csv.writer(f)
        while start < id_length:
            retrieve_tracks = self.sp.audio_features(list(self.user_tracks_id)[start:start+iter])
            for i in range(len(retrieve_tracks)):
                [writer.writerow(retrieve_tracks[i][ft] for ft in feature_types)]
                audio_ft[i+start] = [retrieve_tracks[i][ft] for ft in feature_types]
            start += iter
            if id_length - start < 50:
                iter = id_length - start
    def load_training_features(self):
        if os.path.exists(HAP_SAD_FEATURES):
            with open(HAP_SAD_FEATURES, 'r') as f:
                row_count = sum(1 for row in readFile)
                features = f.readlines()
                self.training_audio_features = np.zeros([row_count, len(feature_types)], dtype = np.float32)
                index = 0
                for feature in features:
                    self.training_audio_features[index] = feature
                    index += 1
        else:
            all_playlist = []
            txt_files = [HAPPY_PATH, SAD_PATH]
            for fi in txt_files:
                with open(fi, 'r') as f:
                    playlist = f.readlines()
                    temp = [line for line in playlist]
                    all_playlist.append(temp)
            for playlist in all_playlist:
                mood_playlist = self.load_training_tracks(playlist)
                self.training_tracks_id.append(mood_playlist)

            for i in range(len(All_Tracks)-1):
                for j in range(i+1, len(All_Tracks)):
                    intersections = list(set(All_Tracks[i]) & set(All_Tracks[j]))
                    for dupes in intersections:
                        #Remove all duplicates found
                        All_Tracks[i].remove(dupes)
                        All_Tracks[j].remove(dupes)
