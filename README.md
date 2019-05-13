#playlist_classifer


fetch_songs -> get_features -> trainednetwork -> create_playlist 
Steps
0. the program will initiate in the network file
1. User will input their username, then will prompt to give authority to the program to read and write into their account
2. the network will call upon the fetch_songs file in order to get the IDs of all the songs in the user playlist 
3. Then, the network will call the get_features file to get the audio features of each ID that was recorded 
4. The network file will then run each ID/audio feature into the neural network, then it will output what type of song it is
5. After the network computation is done for all the users tracks, it will call create_playlist, then it will create multiple playlist and will put corresponding tracks into the playlist that the network decided 


The network must be trained via spotify playlist songs, where each track is unique to its category
Goal :
Have up to 15,000 songs 
Validation will have 1,000 songs or so depending on how it goes 
