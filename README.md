User can have their song library divided up into a Workout and Study playlist or Happy and Sad Playlist.
Used spotipy API to retrieve user's tracks and to create playlist to add the tracks. 
Used a SVM to model the data and trained on ~8000 songs for  Workout&Study and Happy&Sad playlist (~17000 total) 
Training data was gotten from public playlist uploaded by other users. 
The Workout&Study model had an accuracy of 95.85% while the Happy&Sad model had an accuracy of 85.5%. 
Used Libraries: spotipy=2.0, sklearn=0.21.0, numpy=1.15.4
