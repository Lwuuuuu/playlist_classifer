import sys
import spotipy
import spotipy.util as util
import os
import fetch_songs as fs
import random
import numpy as np
import csv
from sklearn.model_selection import train_test_split
STUDY_PATH = os.getcwd() + '/data/Study.txt'
WORKOUT_PATH = os.getcwd() + '/data/Workout.txt'
HAPPY_PATH = os.getcwd() + '/data/Happy.txt'
SAD_PATH = os.getcwd() + '/data/Sad.txt'
HAP_SAD_FEATURES = os.getcwd() + '/data/features_happy_sad.csv'
WORK_STUDY_FEATURES = os.getcwd() + '/data/features_work_study.csv'
class features():
    def __init__(self, sp, id_no, classifcation = None):
        self.sp = sp
        self.id = id_no
        self.danceability = 0
        self.energy = 0
        self.key = 0
        self.loudness = 0
        self.mode = 0
        self.speechiness = 0
        self.acousticness = 0
        self.instrumentalness = 0
        self.valence = 0
        self.tempo = 0
        self.time_signature = 0
        self.classifcation = classifcation
    def audio_features(self):
        features = self.sp.audio_features(str(self.id))[0]
        self.danceability = features['danceability']
        self.energy = features['energy']
        self.key = features['key']
        self.loudness = features['loudness']
        self.mode = features['mode']
        self.speechiness = features['speechiness']
        self.acousticness = features['acousticness']
        self.instrumentalness = features['instrumentalness']
        self.valence = features['valence']
        self.tempo = features['tempo']
        self.time_signature = features['time_signature']
    def return_features(self):
        #Returns 12 Things
        return self.danceability, self.energy, self.key, self.loudness, self.mode, self.speechiness, self.acousticness, self.instrumentalness, self.valence, self.tempo, self.time_signature, self.classifcation

def count_rows(split_choice = 0):
    if split_choice == 0: f = WORK_STUDY_FEATURES
    elif split_choice == 1: f = HAP_SAD_FEATURES
    #Count the number of tracks recorded in the features.CSV
    with open(f, 'r') as readFile:
        row_count = sum(1 for row in readFile)
        return row_count

def retrieve_Playlist(split_choice = 0):
     All_Playlist = []
     #All mood playlist
     if split_choice ==  0: txt_files = [WORKOUT_PATH, STUDY_PATH]
     elif split_choice ==  1: txt_files = [HAPPY_PATH, SAD_PATH]
     for fi in txt_files:
         with open(fi, 'r') as f:
            temp = []
            reader = f.readlines()
            #Reading in the URLs for each mood file into temp
            [temp.append(line) for line in reader]
            #All_Playlist is a list containing list of URLs for each mood playlist
            All_Playlist.append(temp)
     return All_Playlist

def generate_audio_features(username, split_choice = 0, test_size = .1):
    try:
        #If the audio features are already loaded into the CSV file
        if split_choice == 0: f = WORK_STUDY_FEATURES
        elif split_choice == 1: f = HAPPY_SAD_FEATURES
        with open(f, 'r') as readFile:
                index = 0
                print("Reading from CSV file...")
                row_count = count_rows(split_choice)
                #Init the np array
                features_list = np.zeros([row_count, 9], dtype = np.float32)
                reader = csv.reader(readFile)
                csv_file  = list(reader)
                i = 0
                for track in csv_file:
                    #Cut out the following features... [Key, Mode, Time_Signature]
                    track = track[0:2] + track[3:4] + track[5:10]  + track[11:]
                    #Store the audio features into the np array
                    features_list[index] = track
                    index += 1
                #Up to 8th index is are the features, last index is the label
                random.shuffle(features_list)
                return features_list[:, :8], features_list[:, -1]
    except:
        #If no audio features have been loaded into the CSV file
        print("No CSV Found, Creating a CSV...")
        token = fs.get_token(user = "", scope = 'user-library-read')
        if token:
            sp = spotipy.Spotify(auth = token)
            #All_Playlist is a list that contains all URLs to training songs, order is Workout, Study or Happy, Sad
            All_Playlist = retrieve_Playlist(split_choice)
            #total_length will be the total number of tracks in the CSV file, (Need for numpy initialization)
            total_length = 0
            #All tracks contains all the IDs for all playlist
            All_Tracks = []
            for playlist in All_Playlist:
                #mood_Playlist will contain the IDs for all the tracks within that mood
                mood_playlist = fs.training_songs(sp, playlist)
                All_Tracks.append(mood_playlist)
            #Need to get rid of songs that appear in 2+ mood playlist
            #Each mood playlist will now have unique tracks, meaning no other playlist will have that track
            for i in range(len(All_Tracks)-1):
                for j in range(i+1, len(All_Tracks)):
                    intersections = list(set(All_Tracks[i]) & set(All_Tracks[j]))
                    for dupes in intersections:
                        #Remove all duplicates found
                        #print("Found duplicate ID {0} in playlist {1} and playlist {2}".format(dupes, i, j))
                        All_Tracks[i].remove(dupes)
                        All_Tracks[j].remove(dupes)
            mood_no = 0
            np_index = 0
            if split_choice == 0: csv_file = WORK_STUDY_FEATURES
            elif split_choice == 1: csv_file = HAP_SAD_FEATURES
            #Open up the features.CSV so that we can write into it
            f = open(csv_file, 'a')
            writer = csv.writer(f)
            for mood_playlist in All_Tracks:
                for id_no in mood_playlist:
                    #Classifcation is Workout = 0, Study = 1 and  Happy = 0, Sad = 1
                    mood_classifcation = mood_no
                    #Create object that holds all audio features
                    ft = features(sp, id_no, mood_classifcation)
                    #Loads in audio features into object
                    ft.audio_features()
                    #Returns a list containing all the audio features
                    feature = ft.return_features()
                    #Add that audio feature into the np array
                    writer.writerow(feature)
                    print("Track", np_index)
                    np_index += 1
                #Change the mood_no for each mood playlist
                mood_no += 1
            #Closing the file
            f.close()
            #Now that all audio features are loaded into CSV file the try will succeed
            generate_audio_features(split_choice)
        else:
            print("Invalid Username")
            return 0
