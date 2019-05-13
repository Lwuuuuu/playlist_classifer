import sys
import spotipy
import spotipy.util as util
import fetch_songs as fs

class features():
    def __init__(self, sp, id, type = None):
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
        self.type = type
    def set_type(self, type):
        self.type = type
    def audio_features(self):
        features = self.sp.audio_features(str(id))[0]
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
        return [self.danceability, self.energy, self.key, self.loudness, self.mode, self.speechiness,
                self.acousticness, self.instrumentalness, self.valence, self.tempo, self.time_signature, self.type]
def generate_audio_features():
    master_list, _ = fs.run()
    token = fs.get_token(user = "cv2f8pc6v4yqhx9qsgiiynji5", scope = 'user-library-read')
    if token:
        features_list = []
        sp = spotipy.Spotify(auth = token)
        for id in master_list:
            ft = features(id)
            ft.audio_features()
            features_list.append(ft.return_features())
    else:
        print("Invalid")
        return 0
