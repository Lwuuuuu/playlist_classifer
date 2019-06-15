import matplotlib.pyplot as plt
import os
import csv
import random
from functools import reduce
import numpy as np
from gather_features import Spotify
from sklearn import svm, neighbors, linear_model, preprocessing
from sklearn.model_selection import cross_val_score, train_test_split
import pickle
user_file = os.getcwd() + '/data/user.csv'
#Happy is 0 and Sad is 1
feature_types = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
'valence', 'tempo']
feature_dict = {'danceability': [0, 1, 100],
                'energy': [0, 1, 100],
                'loudness': [-60, 0, 100],
                'speechiness': [0, 1, 100],
                'acousticness': [0, 1, 100],
                'instrumentalness': [0, 1, 100],
                'valence': [0, 1, 100],
                 'tempo': [0, 300, 100]
                 }

HAP_SAD_FEATURES = os.getcwd() + '/data/features_happy_sad.csv'

def train_plot():
    with open(HAP_SAD_FEATURES, newline = '') as f:
        reader = csv.reader(f)
        Happy_Length = Sad_Length = 0
        H_index = S_index = 0
        for item in reader:
            if int(item[-1]) == 0:
                 Happy_Length += 1
            else:
                Sad_Length += 1
        Happy_Dataset = np.zeros([Happy_Length, len(feature_dict)], dtype = np.float32)
        Sad_Dataset = np.zeros([Sad_Length, len(feature_dict)], dtype = np.float32)
        f.seek(0, 0)
        for audio_feature in reader:
            if int(audio_feature[-1]) == 0:
                Happy_Dataset[H_index] = audio_feature[:-1]
                H_index += 1
            else:
                Sad_Dataset[S_index] = audio_feature[:-1]
                S_index += 1
        index = 0
        for feature in feature_dict:
            print("Happy %s %f" %(feature, np.average(Happy_Dataset[:, index])))
            print("Sad %s %f" %(feature, np.average(Sad_Dataset[:, index])))
            minimum, maximum, spacing = feature_dict[feature]
            bins = np.linspace(minimum, maximum, spacing)
            plt.hist(Happy_Dataset[:, index], bins, alpha = 0.5, label = 'Happy')
            plt.hist(Sad_Dataset[:, index], bins, alpha = 0.5, label = 'Sad')
            plt.legend(loc='upper right')
            plt.title(feature)
            plt.show()
            index += 1
def user_plot(Other_Dataset = None):
    if not os.path.exists(user_file):
        writeCSV = Spotify('cv2f8pc6v4yqhx9qsgiiynji5')
        writeCSV.load_user_features()
    else:
        with open(user_file, newline = '') as f:
            reader = csv.reader(f)
            row_count = sum(1 for row in reader)
            User_Dataset = np.zeros([row_count, len(feature_dict)], dtype = np.float32)
            f.seek(0, 0)
            i = index = 0
            for audio_feature in reader:
                User_Dataset[i] = audio_feature
                i += 1
            for feature in feature_dict:
                minimum, maximum, spacing = feature_dict[feature]
                bins = np.linspace(minimum, maximum, spacing)
                plt.hist(User_Dataset[:, index], bins, alpha = 0.5, label = 'User')
                if Other_Dataset is not None:
                    plt.hist(Other_Dataset[:, index], bins, alpha = 0.5, label = 'Other')
                plt.legend(loc='upper right')
                plt.title(feature)
                plt.show()
                index += 1

if __name__ == '__main__':
   user_plot()