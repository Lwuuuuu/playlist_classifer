from sklearn import svm, preprocessing
#from sklearn.cross_validation import train_test_split
from get_features import generate_audio_features
import get_features as gf
import numpy as np
import fetch_songs as fs
import csv
import spotipy
import spotipy.util as util
def predict(user_list, id_list, sp):
    #x, y = generate_audio_features()
    X_train, X_test, Y_train, Y_test = generate_audio_features()

    clf = svm.SVC(gamma = 'auto')
    clf.fit(X_train, Y_train)

    accuracy = clf.score(X_test, Y_test)
    print("Accuracy", accuracy)
    work = 0
    study = 0
    for track_features, track_id in zip(user_list, id_list):
        user_test = np.array(track_features, dtype = np.float32)
        user_test = user_test.reshape(1, -1)
        prediction = clf.predict(user_test)
        if prediction == 1:
            mood = "Work"
            work += 1
        else:
            mood = "Study/Chill"
            study += 1
        trackName = sp.track(track_id)['name']
        print("{0} belongs in the {1} playlist.".format(trackName, mood))
    print("{0} songs in Work and {1} songs in Study".format(work, study))

if __name__ == '__main__':
    user_list = list(fs.get_user_songs())
    prediction_list = []
    id_list = []
    token = fs.get_token(user = "cv2f8pc6v4yqhx9qsgiiynji5", scope = 'user-library-read')
    sp = spotipy.Spotify(auth = token)
    i = 0
    for track in user_list:
        result = str("".join(track))
        print(result)
        id_list.append(result)
        feature = gf.features(sp, result)
        feature.audio_features()
        ft = feature.return_features()[:-1]
        print(ft)
        i += 1
        prediction_list.append([ft])
    predict(prediction_list, id_list, sp)


