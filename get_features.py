import sys
import spotipy
import spotipy.util as util
import os
import fetch_songs as fs
import random
import numpy as np
import csv
from sklearn.model_selection import train_test_split
HAPPY_PATH = os.getcwd() + '/data/Happy.txt'
SAD_PATH = os.getcwd() + '/data/Sad.txt'
HAP_SAD_FEATURES = os.getcwd() + '/data/features_happy_sad.csv'

def count_rows(split_choice = 0):
    #Count the number of tracks recorded in the features.CSV
    with open(f, 'r') as readFile:
        row_count = sum(1 for row in readFile)
        return row_count

def retrieve_Playlist(split_choice = 0):
     All_Playlist = []
     #All mood playlist
     txt_files = [HAPPY_PATH, SAD_PATH]
     for fi in txt_files:
         with open(fi, 'r') as f:
            temp = []
            reader = f.readlines()
            #Reading in the URLs for each mood file into temp
            [temp.append(line) for line in reader]
            #All_Playlist is a list containing list of URLs for each mood playlist
            All_Playlist.append(temp)
     return All_Playlist

def generate_audio_features(username, test_size = .1):
    try:
        #If the audio features are already loaded into the CSV file
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
            csv_file = HAP_SAD_FEATURES
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
