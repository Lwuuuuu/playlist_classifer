import sys
import spotipy
import spotipy.util as util
import os
import fetch_songs as fs
import random
import numpy as np
import csv
import time
import json 
import math
import random
from tqdm import tqdm
import pickle
from collections import defaultdict, Counter
from classifcation import mood_predictor, recommender_predictor, drop
#import classifcation  as cn 
#Happy is 0 and Sad is 1
GLOBAL_SCOPE = 'user-library-modify playlist-modify-private user-library-read playlist-read-private'
feature_types = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
'valence', 'tempo']
HAPPY_PATH = os.getcwd() + '/data/Happy.txt'
SAD_PATH = os.getcwd() + '/data/Sad.txt'
user_file = os.getcwd() + '/data/user.csv'
HAP_SAD_FEATURES = os.getcwd() + '/data/features_happy_sad.csv'
GENRE_DICT = os.getcwd() + '/data/genre_dict.json'
class Spotify():
    def __init__(self, username, max_tracks):
        self.max_tracks = max_tracks
        self.username = username
        self.token = self.get_token(GLOBAL_SCOPE)
        self.sp = spotipy.Spotify(auth = self.token)
        self.user_tracks_id = []
        self.user_audio_features = None
        self.training_tracks_id = []
        self.training_audio_features = None
        self.artist_dict = defaultdict(int)
        self.genre_dict = defaultdict(int)
        self.user_track_uris = set()
        self.user_playlist_track_uri = set()
    def get_sp(self):
        return self.sp

    def get_user_ids(self):
        return self.user_tracks_id

    def get_token(self, scope):
        token = util.prompt_for_user_token(username = self.username, scope = scope, client_id='1da08e2fb3994edebbf758e0fa0ab23b',
        client_secret='98fe97db700b44f4ad0743b945e3084b',redirect_uri='http://localhost:8888/callback/')
        return token

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
            for track in user_songs:
                self.user_tracks_id.append(track['track']['id'])
                self.user_track_uris.add(track['track']['uri'])

    def load_training_tracks(self, Training_Playlist):
        mood_playlist = set()
        #For all spotify playlist that is listed
        total = 0
        for playlist_info in Training_Playlist:
            index = 0
            while 1:
                #Strip because need to get rid of the whitespaces in the playlist_info string
                results = self.sp.user_playlist_tracks('', playlist_id = playlist_info.strip(), limit = 100, offset = index)
                tracks = results['items']
                length = len(tracks)
                if length == 0: break
                index += length
                total += length
                print("ID :", total)
                #Adds the tracks ID to the set
                [mood_playlist.add(track_id['track']['id']) for track_id in tracks]
        return list(mood_playlist)

    def load_user_features(self):
        if os.path.exists(user_file):
            with open(user_file, 'r') as fi:
                row_count = sum(1 for row in fi)
            with open(user_file, newline = '') as f:
                reader = csv.reader(f)
                self.user_audio_features = np.zeros([row_count, len(feature_types)], dtype = np.float32)
                index = 0
                for feature in reader:
                    self.user_audio_features[index] = feature
                    index += 1
        else:
            self.load_user_tracks()
            id_length = len(self.user_tracks_id)
            self.user_audio_features = np.zeros([id_length, len(feature_types)], dtype = np.float32)
            start = 0
            if id_length <= 50:
                iter = id_length
            else:
                iter = 50
            f = open(user_file, 'a', newline = '')
            writer = csv.writer(f)
            while start < id_length:
                retrieve_tracks = self.sp.audio_features(self.user_tracks_id[start:start+iter])
                for i in range(len(retrieve_tracks)):
                    track_features = [retrieve_tracks[i][ft] for ft in feature_types]
                    writer.writerow(track_features)
                    self.user_audio_features[i+start] = track_features
                start += iter
                if id_length - start < 50:
                    iter = id_length - start
        return self.user_audio_features

    def generate_training_features(self):
        total_id = sum([len(self.training_tracks_id[l]) for l in range(len(self.training_tracks_id))])
        print("TOTAL", total_id)
        self.training_audio_features = np.zeros([total_id, len(feature_types)+1], dtype = np.float32)
        for mood in range(len(self.training_tracks_id)):
            id_length = len(self.training_tracks_id[mood])
            start = 0
            if id_length <= 50:
                iter = id_length
            else:
                iter = 50
            f = open(HAP_SAD_FEATURES, 'a', newline='')
            writer = csv.writer(f)
            while start < id_length:
                retrieve_tracks = self.sp.audio_features(self.training_tracks_id[mood][start:start+iter])
                for i in range(len(retrieve_tracks)):
                    temp = [retrieve_tracks[i][ft] for ft in feature_types]
                    temp.append(mood)
                    self.training_audio_features[i+start] = temp
                    writer.writerow(temp)
                start += iter
                print("Track: ", start)
                if id_length - start < 50:
                    iter = id_length - start
            f.close()

    def load_training_features(self):
        if os.path.exists(HAP_SAD_FEATURES):
            with open(HAP_SAD_FEATURES, 'r') as fi:
                row_count = sum(1 for row in fi)
            with open(HAP_SAD_FEATURES, newline = '') as f:
                reader = csv.reader(f)
                self.training_audio_features = np.zeros([row_count, len(feature_types)+1], dtype = np.float32)
                index = 0
                for feature in reader:
                    self.training_audio_features[index] = feature
                    index += 1
                return self.training_audio_features
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
            for i in range(len(self.training_tracks_id)-1):
                for j in range(i+1, len(self.training_tracks_id)):
                    intersections = list(set(self.training_tracks_id[i]) & set(self.training_tracks_id[j]))
                    for dupes in intersections:
                        #Remove all duplicates found
                        self.training_tracks_id[i].remove(dupes)
                        self.training_tracks_id[j].remove(dupes)
            self.generate_training_features()
            return self.training_audio_features
            
    def load_playlist_features(self, URL):
        ids = []
        #For all spotify playlist that is listed
        index = 0
        while 1:
            #Strip because need to get rid of the whitespaces in the playlist_info string
            results = self.sp.user_playlist_tracks('', playlist_id = URL, limit = 100, offset = index)
            tracks = results['items']
            length = len(tracks)
            if length == 0: break
            index += length
            #Adds the tracks ID to the set
            [ids.append(track_id['track']['id']) for track_id in tracks]
        while 1: 
            #Get rid of tracks whoses IDs were unretrievable 
            try:
                ids.remove(None)
            except:
                break
        id_length = len(ids)
        playlist = np.zeros([id_length, len(feature_types)], dtype = np.float32)
        start = 0
        if id_length <= 50:
            iter = id_length
        else:
            iter = 50
        while start < id_length:
            retrieve_tracks = self.sp.audio_features(ids[start:start+iter])
            for i in range(len(retrieve_tracks)):
                track_features = [retrieve_tracks[i][ft] for ft in feature_types]
                playlist[i+start] = track_features
            start += iter
            if id_length - start < 50:
                iter = id_length - start
        return playlist, ids
    def track_genres(self):
        print("Parsing User Tracks")
        self.load_user_tracks()
        print("Parsing User Playlist Tracks")
        self.user_playlist_tracks()
        if os.path.exists(GENRE_DICT) == False:
            start = 0 
            user_length = len(self.user_tracks_id)
            index = 50 
            pbar = tqdm(total = user_length, initial = start)
            while start < user_length:
                results = self.sp.tracks(self.user_tracks_id[start:start+index])
                for i in range(len(results)):
                    artists = results['tracks'][i]['album']['artists']
                    for j in range(len(artists)):
                        self.artist_dict[artists[j]['id']] += 1     
                start += len(results)
                pbar.update(start)  
                if user_length - start < 50:
                    index = user_length - start
            pbar.close()
            
            for artist in tqdm(self.artist_dict):
                genres = self.sp.artist(artist)['genres']
                for i in range(len(genres)):
                    self.genre_dict[genres[i]] += self.artist_dict[artist]
            self.genre_dict = Counter(self.genre_dict).most_common(5) 
            with open(GENRE_DICT, 'w') as fp:
                json.dump(self.genre_dict, fp)
        else:
            with open(GENRE_DICT, 'r') as fp:
                self.genre_dict = json.load(fp)
        user_genre_total = sum(x[1] for x in self.genre_dict)
        recHappy = []
        recSad = []
        current_no = 0 
        pbar = tqdm(total = self.max_tracks, initial = 0)
        print("\nParsing Genre Tracks...")
        parsed_uris = set()
        for x in self.genre_dict:
            search_string = 'genre:"{0}"'.format(x[0])
            index = 0  
            genre_max = math.ceil(x[1]/user_genre_total * self.max_tracks)
            notEnough = True 
            happy_buffer = []
            sad_buffer = []
            genre_id_list = []
            print("\nGenre {} MAX - {} ".format(x[0], genre_max))
            while notEnough:
                results = self.sp.search(q=search_string, limit = 10, offset=index, type = 'track')['tracks']['items']
                index += len(results)
                for i in range(len(results)):
                    genre_id_list.append(results[i]['id']) 
                if len(genre_id_list) % 500 == 0:
                    ret = []
                    for i in range(10): 
                        genre_ft = self.sp.audio_features(genre_id_list[i*50:(i+1)*50])
                        for j in range(len(genre_ft)):
                            ret.append(genre_ft[j])
                    random.shuffle(ret)
                    genre_audio_features = np.zeros([len(genre_id_list), len(feature_types)])
                    for i in range(len(ret)):
                        genre_audio_features[i] = [ret[i][ft] for ft in feature_types]
                    recTracks, _ = recommender_predictor(genre_id_list, genre_audio_features)
                    genre_id_list = []
                    ids = [] 
                    recfeatures = np.zeros([len(recTracks), len(feature_types)])
                    for i in range(len(recTracks)):
                        ids.append(recTracks[i][0])
                        recfeatures[i] = recTracks[i][1]
                    recfeatures = drop(recfeatures, 'loudness')
                    recfeatures = drop(recfeatures, 'speechiness')
                    if len(ids) > 0: 
                        genre_recHappy, genre_recSad = mood_predictor(ids, recfeatures)
                    for track in genre_recHappy:
                        uri = self.sp.track(track)['uri']
                        if uri not in list(self.user_track_uris | self.user_playlist_track_uri | parsed_uris):
                            happy_buffer.append(track) 
                            parsed_uris.add(uri)
                    for track in genre_recSad:
                        uri = self.sp.track(track)['uri']
                        if uri not in list(self.user_track_uris | self.user_playlist_track_uri | parsed_uris):
                            sad_buffer.append(track)
                            parsed_uris.add(uri) 
                    print("Found {} Happy Tracks and {} Sad Tracks in {} Genre".format(len(happy_buffer), len(sad_buffer), x[0]))
                    if len(happy_buffer) and len(sad_buffer) >= genre_max: 
                        pbar.update(genre_max)
                        for i in range(genre_max):
                            recSad.append(sad_buffer[i])
                            recHappy.append(happy_buffer[i])
                        notEnough = False
        return recHappy, recSad
    def user_playlist_tracks(self): 
        results = self.sp.current_user_playlists()['items']
        for i in range(len(results)):
            index = 0 
            while 1:
                tracks = self.sp.user_playlist_tracks(user = self.username, playlist_id = results[i]['id'], offset = index)['items']
                index += len(tracks)
                if len(tracks) == 0:
                    break
                for j in range(len(tracks)):
                    self.user_playlist_track_uri.add(tracks[j]['track']['uri'])
        return self.user_playlist_track_uri
    def create_playlist(self, IDs, playlistName):
        playlistID = self.sp.user_playlist_create(user = self.username, name = playlistName, public = False)
        self.sp.user_playlist_add_tracks(user = self.username, playlist_id = playlistID['id'], tracks = IDs)
        print("\nSuccessfully Created Playlist")

if __name__ == '__main__':
    max_tracks = int(input("Enter how many tracks you want in your playlists: "))
    test = Spotify('cv2f8pc6v4yqhx9qsgiiynji5', max_tracks)
    test.user_playlist_tracks()
    recHappy, recSad = test.track_genres()
    test.create_playlist(recHappy, 'Recommended Happy')
    test.create_playlist(recSad, 'Recommended Sad')