User can have their song library divided up into a Workout and Study playlist or Happy and Sad Playlist.
User can also provide a Spotify URL and it will classify each song to be for Happy/Sad or WorkoutStudy. 
Used spotipy API to retrieve user's tracks and to create playlist to add the tracks. 
Used a SVM to model the data and trained on ~8600 songs for Workout&Study and 9500 Happy&Sad songs (~18000 total) 
Training data was gotten from public playlist uploaded by other users. 
The Workout&Study model had an accuracy of 95.85% while the Happy&Sad model had an accuracy of 85.5%. 
Used Libraries: spotipy=2.0, sklearn=0.21.0, numpy=1.15.4
