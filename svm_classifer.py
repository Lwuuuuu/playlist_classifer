from sklearn import svm, preprocessing, neighbors
#from sklearn.cross_validation import train_test_split
from get_features import generate_audio_features
import get_features as gf
import numpy as np
import fetch_songs as fs
import csv
import spotipy
import spotipy.util as util
def predict(user_list, id_list, sp, choice = 0):
    #Generate the training and testing data
    X_train, X_test, Y_train, Y_test = generate_audio_features(txt = choice, test_size = .2)
    #clf = neighbors.KNeighborsClassifier(n_jobs = 1)
    clf = svm.SVC(gamma = 'auto', decision_function_shape = 'ovr')

    #Train the model with X_train and Y_train
    clf.fit(X_train, Y_train)

    #Test the model against the X_test and Y_test
    accuracy = clf.score(X_test, Y_test)
    print("Accuracy", accuracy)
    type1 = type2 = 0
    if choice == 0:
        mood_dict = {'Workout' : [],
                    'Study' : []
                    }
    if choice == 1:
        mood_dict = {'Happy' : [],
                    'Sad' : []
                    }
    for track_features, track_id in zip(user_list, id_list):
        #Store the audio_features into an np array, since that is the format needed to past into predict
        user_test = np.array(track_features, dtype = np.float32)
        #Reshaping
        user_test = user_test.reshape(1, -1)
        #Will Predict which playlsit this track belongs to
        #Workout = 0, Study = 1, Happy = 0, Sad = 1
        predicted_mood = clf.predict(user_test)
        if predicted_mood == 0 and choice == 0:
            mood = 'Workout'
            mood_dict['Workout'].append(track_id)
            type1 += 1
        if predicted_mood  == 1 and choice == 0:
            mood = "Study"
            mood_dict['Study'].append(track_id)
            type2 += 1
        if predicted_mood == 0 and choice == 1:
            mood = 'Happy'
            mood_dict['Happy'].append(track_id)
            type1 += 1
        if predicted_mood == 1 and choice == 1:
            mood = 'Sad'
            mood_dict['Sad'].append(track_id)
            type2 += 1
        trackName = sp.track(track_id)['name']
        print("{0} belongs in the {1} playlist.".format(trackName, mood))
    print("Type1 - {0},  Type2 - {1}".format(type1, type2))

if __name__ == '__main__':
    #Loads in the current users track list
    user_list = list(fs.get_user_songs())
    prediction_list = []
    id_list = []
    token = fs.get_token(user = "cv2f8pc6v4yqhx9qsgiiynji5", scope = 'user-library-read')
    sp = spotipy.Spotify(auth = token)
    i = 0
    for track in user_list:
        #In the CSV file, the track ID is stored as a list where each element is an indivdiual char.
        #Should of stored as a text file
        result = str("".join(track))
        #Keep a list of all the track IDs, for use in predict()
        id_list.append(result)
        #Loads the audio features for a specific Track ID
        feature = gf.features(sp, result)
        feature.audio_features()
        #Do not include the last element of the list because that is the label, which is None as it is unlabled
        ft = feature.return_features()[:-1]
        ft = ft[0:2] + ft[3:4] + ft[5:10]
        i += 1
        #Save the audio features as a list
        prediction_list.append(list(ft))
    split = int(input("0 for Work&Study, 1 for Happy&Sad: "))
    predict(prediction_list, id_list, sp, choice = split)
