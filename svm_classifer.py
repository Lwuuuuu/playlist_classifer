from sklearn import svm, preprocessing
#from sklearn.cross_validation import train_test_split
from get_features import generate_audio_features
import numpy as np

#x, y = generate_audio_features()
X_train, X_test, Y_train, Y_test = generate_audio_features()

print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)
clf = svm.SVC()
clf.fit(X_train, Y_train)

accuracy = clf.score(X_test, Y_test)
print(accuracy)



