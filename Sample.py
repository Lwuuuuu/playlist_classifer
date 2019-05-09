import sys
import spotipy
import spotipy.util as util
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
Grande = "https://open.spotify.com/artist/66CXWjxzNUsdJxJ2JdwvnR"
TS = "https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02"
Logic = "https://open.spotify.com/artist/4xRYI6VqpkE3UwrDrAZL8L"
Shallou = "https://open.spotify.com/artist/7C3Cbtr2PkH2l4tOGhtCsk"

#Make a program that given a players whole song playlist, it can cateogirze the songs into Working Out, Study/Chill and maybe something else
#Make a classifer that can classify the song, then put that song into the desginated playlist

def difference(main, other):
    difference = defaultdict(float)
    difference['danceability'] = (main[0] - other[0]) / other[0] * 100
    difference['energy'] = (main[1] - other[1]) / other[1] * 100
    difference['key'] = (main[2] - other[2]) / other[2] * 100
    difference['loudness'] = (main[3] - other[3]) / other[3] * 100
    difference['mode'] = (main[4] - other[4]) / other[4] * 100
    difference['speechiness'] = (main[5] - other[5]) / other[5] * 100
    difference['acousticness'] = (main[6] - other[6]) / other[6] * 100
    difference['instrumentalness'] = (main[7] - other[7]) / other[7] * 100
    difference['liveness'] = (main[8] - other[8]) / other[8] * 100
    difference['valence'] = (main[9] - other[9]) / other[9] * 100
    difference['tempo'] = (main[10] - other[10]) / other[10] * 100
    difference['time_signature'] = (main[11] - other[11]) / other[11] * 100
    for item in difference:
        print(item, difference[item])
    return difference
def get_tracks_id(token, art_id):
    sp = spotipy.Spotify(auth=token)
    Track_List = set()
    index = 0
    while 1:
        SC = "https://open.spotify.com/artist/4Mc3zbnQx4wRb0tYg7A8sG"
        bone = "https://open.spotify.com/artist/4jGPdu95icCKVF31CcFKbS"
        results = sp.artist_albums(artist_id = art_id, limit = 50, offset = index)
        #List of Albums by the artist_Id
        Albums = results['items']
        index += len(Albums)
        #If no more avaliable albums to query
        if len(Albums) == 0:
            break
        for i in range(len(Albums)):
            #Queries out the albums ID
            ID = [Albums[i]['id']]
            #print("ID", ID)
            Album = sp.albums(ID)
            #Album Dictonary
            Tracks = Album['albums'][0]['tracks']['items']
            for j in range(len(Tracks)):
                #Gets the name of each track in the album
                Track_List.add(Tracks[j]['id'])
                #print(Tracks[j]['href'])
    #for track in Track_List:
    #    print(track)
    print("# of Songs", len(Track_List))
    return Track_List, len(Track_List)
def top_tracks(token):
    popular_tracks = set()
    sp = spotipy.Spotify(auth=token)
    results = sp.artist_top_tracks(artist_id = Grande)
    tracks = results['tracks']
    for song in tracks:
        popular_tracks.add((song['name']))
        #print(song['name'])
    return popular_tracks

def features(token, track_id, Length):
    feature_list = [0] * 12
    sp = spotipy.Spotify(auth=token)
    i = 0
    for id in track_id:
        print("Track", i)
        features = sp.audio_features(id)
        feature_list[0] += features[0]['danceability']
        feature_list[1] += features[0]['energy']
        feature_list[2] += features[0]['key']
        feature_list[3] += features[0]['loudness']
        feature_list[4] += features[0]['mode']
        feature_list[5] += features[0]['speechiness']
        feature_list[6] += features[0]['acousticness']
        feature_list[7] += features[0]['instrumentalness']
        feature_list[8] += features[0]['liveness']
        feature_list[9] += features[0]['valence']
        feature_list[10] += features[0]['tempo'] / 100
        feature_list[11] += features[0]['time_signature']
        i += 1
    for i in range(len(feature_list)):
        feature_list[i] = feature_list[i] / Length
    # objects = ('danceability', 'energy', 'key', 'loudness', 'mode',
    # 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
    # 'valence', 'tempo', 'time_signature')
    # y_pos = np.arange(len(objects))
    # plt.bar(y_pos, feature_list, align = 'center', alpha = 0.5)
    # plt.xticks(y_pos, objects)
    # plt.ylabel('Value')
    # plt.title('Features')
    return feature_list
    #plt.show()
def new_release(token):
    sp = spotipy.Spotify(auth=token)
    of = 0
    New_Release_Albums = set()
    total_tracks = 0
    while 1:
        results = sp.new_releases(country = 'US', limit = 50, offset = of)
        Albums = results['albums']['items']
        Length = len(Albums)
        if Length == 0:
            break
        of += Length
        for i in range(len(Albums)):
            New_Release_Albums.add(Albums[i]['name'])
            total_tracks += Albums[i]['total_tracks']
    print("Total Tracks on New Releases", total_tracks)
    return New_Release_Albums
def get_user_songs(token):
    user_songs_id = set()
    index = 0
    sp = spotipy.Spotify(auth=token)
    while 1:
        results = sp.current_user_saved_tracks(limit=20, offset=index)
        user_songs = results['items']
        length = len(user_songs)
        if length == 0:
            break
        index += length
        for track in user_songs:
            user_songs_id.add(track['track']['id'])
            print(track['track']['id'])
    return user_songs_id
username = ""
#username = input("Enter UserName: ")
token = util.prompt_for_user_token(username,'user-library-read',client_id='1da08e2fb3994edebbf758e0fa0ab23b',
client_secret='98fe97db700b44f4ad0743b945e3084b',redirect_uri='http://localhost:8888/callback/')
if token:
    get_user_songs(token)
    #new_release(token)
    #top_tracks(token)
    # main_track_id, main_length = get_tracks_id(token, Shallou)
    # main_feature_list = features(token, main_track_id, main_length)
    # other_track_id, other_length = get_tracks_id(token, TS)
    # other_feature_list = features(token, other_track_id, other_length)
    # difference(main_feature_list, other_feature_list)
else:
    print("Can't get token for", username)
