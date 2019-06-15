from sklearn import svm, neighbors, linear_model, preprocessing
from sklearn.model_selection import cross_val_score, train_test_split
from gather_features import Spotify
import numpy as np
import random
import os 
import pickle
from tqdm import tqdm
#Happy is 0, Sad is 1 
#Dislike 0, Like is 1
recModel_PATH = os.getcwd() + '/data/recModel.sav'
moodModel_PATH = os.getcwd() + '/data/moodModel.sav'
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


def mean_std(np_array):
    data_points = np_array.shape[1]
    mu_sigma = np.zeros([data_points, 2], dtype = np.float32)
    for i in range(data_points):
        mean = np.mean(np_array[:, i])
        std_dev = np.std(np_array[:, i])
        mu_sigma[i] = [mean, std_dev]
    return mu_sigma

def random_picker(Lower_Interval, Upper_Interval):
    min_range = Lower_Interval[1] - Lower_Interval[0]
    max_range = Upper_Interval[1] - Upper_Interval[0]
    which_interval = random.uniform(0, min_range+max_range)
    if which_interval <= min_range:
        num = random.uniform(Lower_Interval[0], Lower_Interval[1])
    else:
        num = random.uniform(Upper_Interval[0], Upper_Interval[1])
    return num

def generate_features(mu_sigma, iters, inter):
    #Fake Numbers are 1-2 standard deviations away
    num_features = mu_sigma.shape[0]
    generated_features = np.zeros([iters, num_features])
    for i in tqdm(range(iters)):
        j = 0
        for feature in feature_dict:
            lower_interval = []
            upper_interval = []
            lower_interval.append(mu_sigma[j][0] - inter[1] * mu_sigma[j][1])
            lower_interval.append(mu_sigma[j][0] - inter[0] * mu_sigma[j][1])
            upper_interval.append(mu_sigma[j][0] + inter[0] * mu_sigma[j][1])
            upper_interval.append(mu_sigma[j][0] + inter[1] *  mu_sigma[j][1])
            if lower_interval[0] < feature_dict[feature][0]:
                lower_interval[0] = feature_dict[feature][0]
            if lower_interval[1] < feature_dict[feature][0]:
                lower_interval[1] = feature_dict[feature][0]
            if upper_interval[0] > feature_dict[feature][1]:
                upper_interval[0] = feature_dict[feature][1]
            if upper_interval[1] > feature_dict[feature][1]:
                upper_interval[1] = feature_dict[feature][1]
            rand_number = random_picker(lower_interval, upper_interval)
            generated_features[i, j] = rand_number
            j += 1
    return generated_features

def drop(np_array, feature):
    index = feature_types.index(feature)
    return np.concatenate((np_array[:, :index], np_array[:, index+1:]), axis = 1)


def recommender_model(user, fakes):
    user_size = user.shape[0]
    fakes_shape = fakes.shape[0]
    neg = np.zeros([fakes_shape, 1])
    pos = np.ones([user_size, 1])
    neg_examples = np.concatenate((fakes, neg), axis = 1)
    pos_examples = np.concatenate((user, pos), axis = 1)
    Dataset = np.concatenate((neg_examples, pos_examples), axis = 0)

    Dataset = drop(Dataset, 'tempo')

    random.shuffle(Dataset)
    X, y = Dataset[:, :-1], Dataset[:, -1].astype(dtype = int)
    X = preprocessing.normalize(X)
    clf = neighbors.KNeighborsClassifier(n_neighbors = 5, weights = 'distance', p = 2, algorithm = 'ball_tree')
    clf.fit(X, y)
    pickle.dump(clf,open(recModel_PATH, 'wb'))

def mood_model(Dataset):
    random.shuffle(Dataset)
    #Omitting speechiness and loudness, similar histograms index 2 and 3
    Dataset = drop(Dataset, 'loudness')
    Dataset = drop(Dataset, 'speechiness')

    X, y = Dataset[:, :-1], Dataset[:, -1].astype(dtype = int)
    X = preprocessing.normalize(X)

    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    clf = neighbors.KNeighborsClassifier(n_neighbors = 5, weights = 'distance', p = 2, algorithm = 'ball_tree')
    clf.fit(X, y)
    #scores = cross_val_score(clf, X, y, cv = 10)
    #print("Accuracy: %f (+/- %f)" % (scores.mean(), scores.std() * 2))
    pickle.dump(clf, open(moodModel_PATH, 'wb'))

def recommender_predictor(ids, features): #Will return the track IDs of tracks model thinks you like and dislike
    like = []
    dislike = []
    features_omit_tempo = drop(features, 'tempo')
    clf = pickle.load(open(recModel_PATH, 'rb'))
    predictions = clf.predict(features_omit_tempo)
    for x, y, z in zip(ids, predictions, features): #0 is dislike, 1 is like  
        dislike.append([x, z.reshape(1, 8)]) if y == 0 else like.append([x, z.reshape(1, 8)])
    return like, dislike

def mood_predictor(ids, features): #Will return the track IDs of tracks that are happy 
    happy = []
    sad = []
    clf = pickle.load(open(moodModel_PATH, 'rb'))
    predictions = clf.predict(features)
    for x, y in zip(ids, predictions):
        happy.append(x) if y == 0 else sad.append(x)
    return happy, sad

def master(URL):
    songRecommender = Spotify('cv2f8pc6v4yqhx9qsgiiynji5')
    user_tracks = songRecommender.load_user_features()
    if os.path.exists(recModel_PATH) == False:
        mu_sigma =  mean_std(user_tracks)
        unrecommended_interval = [.5, 2]
        unrecommended_tracks = generate_features(mu_sigma, 100000, unrecommended_interval)
        recommended_interval = [0, .5]
        recommended_tracks = generate_features(mu_sigma, 100000, recommended_interval)
        recommender_model(recommended_tracks, unrecommended_tracks)

    features_from_url, ids_from_url = songRecommender.load_playlist_features(URL)
    Recommended_from_URL, _ = recommender_predictor(ids_from_url, features_from_url) #Rec_from_URL = [[ids, [np array of features]], [ids, [np array of features]]]
    if os.path.exists(moodModel_PATH) == False:
        Dataset = songRecommender.load_training_features()
        mood_model(Dataset)
    ids = []
    recLength = len(Recommended_from_URL)
    features = np.zeros([recLength, len(feature_types)])
    for i in range(recLength):
        ids.append(Recommended_from_URL[i][0])
        features[i] = Recommended_from_URL[i][1]
    features = drop(features, 'loudness')
    features = drop(features, 'speechiness')
    recHappy, recSad = mood_predictor(ids, features) 

    sp = songRecommender.get_sp()
    print("Happy Tracks")
    for track in recHappy:
        print(sp.track(track)['name'])
    print("Sad Tracks")
    for track in recSad:
        print(sp.track(track)['name'])
master('https://open.spotify.com/playlist/37i9dQZF1DX5KpP2LN299J')