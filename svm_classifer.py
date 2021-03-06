from sklearn import svm
from sklearn.model_selection import cross_val_score, train_test_split
from get_features import generate_audio_features
import get_features as gf
import numpy as np
import fetch_songs as fs
import csv
import spotipy
import spotipy.util as util
import pickle
import os
GLOBAL_SCOPE = 'user-library-modify playlist-modify-private user-library-read'
MODELHS_PATH = os.getcwd() + '/data/modelHS.sav'
MODELWS_PATH = os.getcwd() + '/data/model.sav'

def accuracy(username):
    #Generate the training and testing data
    X, Y = generate_audio_features(username)
    #Creating SVM, C = 10, gamma = .001 optimal from grid search
    clf = svm.SVC(kernel = 'linear', gamma = .001, decision_function_shape = 'ovr', C = 10)

    #Using cross_val_score to score the model
    scores = cross_val_score(clf, X, Y, cv = 10)
    print("Accuracy: %f (+/- %f)" % (scores.mean(), scores.std() * 2))

def predict(username, sp):
    #Loads in the current users track list
    user_list = fs.get_user_songs(username, sp)
    #Prediction List will hold the audio features of the user's tracks
    prediction_list = []
    #ID List is the list of the IDs of the user's tracks
    id_list = []
    token = fs.get_token(user = username, scope = GLOBAL_SCOPE)
    sp = spotipy.Spotify(auth = token)
    print("Generating tracks audio features...")
    for track in user_list:
        #In the CSV file, the track ID is stored as a list where each element is an indivdiual char.
        id_list.append(track)
        #Loads the audio features for a specific Track ID
        feature = gf.features(sp, track)
        feature.audio_features()
        #Do not include the last element of the list because that is the label, which is None as it is unlabled
        ft = feature.return_features()[:-1]
        #Exclude the following audio_features; Key, Mode and Time_Signature
        ft = ft[0:2] + ft[3:4] + ft[5:10]
        prediction_list.append(list(ft))
    #Load pre-trained model if avaliable
    if os.path.exists(MODELHS_PATH):
        print("Loading into Pre-Trained Model..")
        clf = pickle.load(open(MODELHS_PATH, 'rb'))
    else:
        clf = svm.SVC(kernel = 'linear', gamma = .001, decision_function_shape = 'ovr', C = 10)
        #Load in the training data
        X, Y = generate_audio_features(username, split_choice = choice)
        print("Training the Model.")
        #Train Model
        clf.fit(X, Y)
        print("Writing Model to file...")
        pickle.dump(clf,open(MODELHS_PATH, 'wb'))
    type1 = type2 = 0
    tmp = []
    mood_dict = {'Generated-Happy' : [],
                'Generated-Sad' : []
                }
    for track_features, track_id in zip(prediction_list, id_list):
        user_test = np.array(track_features, dtype = np.float32)
        user_test = user_test.reshape(1, -1)
        #Will Predict which playlsit this track belongs to
        predicted_mood = clf.predict(user_test)
        #Workout = 0, Study = 1, Happy = 0, Sad = 1
        if predicted_mood == 0:
            mood = 'Happy'
            mood_dict['Generated-Happy'].append(track_id)
            type1 += 1
        if predicted_mood == 1:
            mood = 'Sad'
            mood_dict['Generated-Sad'].append(track_id)
            type2 += 1
        trackName = sp.track(track_id)['name']
        print("{0} belongs in the {1} playlist.".format(trackName, mood))
    [tmp.append(x) for x in mood_dict]
    print("{0} - {1},  {2} - {3}".format(tmp[0],type1,tmp[1], type2))
    return mood_dict
