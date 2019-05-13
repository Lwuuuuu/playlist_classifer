import sys
import spotipy
import spotipy.util as util
import fetch_songs as fs
import random
import numpy as np

 #WorkOut
W1 = "https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP"
W2 = "https://open.spotify.com/playlist/37i9dQZF1DXdxcBWuJkbcy"
W3 = "https://open.spotify.com/playlist/37i9dQZF1DWUVpAXiEPK8P"
W4 = "https://open.spotify.com/playlist/37i9dQZF1DWYNSm3Z3MxiM"
W5 = "https://open.spotify.com/playlist/37i9dQZF1DWTl4y3vgJOXW"
W6 = "https://open.spotify.com/playlist/37i9dQZF1DX4eRPd9frC1m"
W7 = "https://open.spotify.com/playlist/37i9dQZF1DXdURFimg6Blm"
W8 = "https://open.spotify.com/playlist/37i9dQZF1DWUSyphfcc6aL"
Workout_Playlist  = [W1, W2, W3, W4, W5, W6, W7, W8]


#Study/Chill
S1 = "https://open.spotify.com/playlist/19uVLpMdgv0Dy3LvpYx4LA"
S2 = "https://open.spotify.com/playlist/37i9dQZF1DX8NTLI2TtZa6"
S3 = "https://open.spotify.com/playlist/0PRs1Xaui4zCv9LdIIt20X"
S4 = "https://open.spotify.com/playlist/37i9dQZF1DX1dvMSwf27JO"
S5 = "https://open.spotify.com/playlist/37i9dQZF1DWSSrwtip3vZP"
S6 = "https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ"
S7 =
Study_Playlist = [S1, S2, S3, S4, S5, S6]
#Upbeat/Fun






class features():
    def __init__(self, sp, id, classifcation = None):
        self.sp = sp
        self.id = id
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
        return self.danceability, self.energy, self.key, self.loudness, self.mode, self.speechiness, self.acousticness, self.instrumentalness, self.valence, self.tempo, self.time_signature, self.classifcation
def generate_audio_features(test_size = .1):
    token = fs.get_token(user = "cv2f8pc6v4yqhx9qsgiiynji5", scope = 'user-library-read')
    if token:
        sp = spotipy.Spotify(auth = token)
        workout_list  = fs.training_songs(sp, Workout_Playlist)
        study_list = fs.training_songs(sp, Study_Playlist)
        features_list = np.zeros([len(workout_list)+len(study_list), 12], dtype = np.float32)
        np_index = 0
        print(len(workout_list))
        for id in workout_list:
            work_classifcation = 1 #Work Label
            ft = features(sp, id, work_classifcation)
            ft.audio_features()
            feature = ft.return_features()
            print(feature)
            feature = np.array(feature)
            features_list[np_index] = feature
            print("Track", np_index)
            np_index += 1
        for id in study_list:
               study_classifcation = 0 #Work Label
               ft = features(sp, id, study_classifcation)
               ft.audio_features()
               feature = ft.return_features()
               print(feature)
               feature = np.array(feature)
               features_list[np_index] = feature
               print("Track", np_index)
               np_index += 1

        random.shuffle(features_list)
        total_length = len(workout_list) + len(study_list)
        testing_size = int(test_size * total_length)
        train_x = (features_list[: , :11][:-testing_size])
        train_y = (features_list[: , -1][:-testing_size])

        test_x = (features_list[: , :11][-testing_size:])
        test_y = (features_list[: , -1][-testing_size:])
        #x = list(features_list[: ,0])
        #y = list(features_list[: ,1])
        return train_x, test_x, train_y, test_y
    else:
        print("Invalid")
        return 0
#if __name__ == '__main__':
    #train_x, train_y, test_x, test_y = generate_audio_features()
