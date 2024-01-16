import numpy as np
import cv2
import pandas as pd # linear algebra
import skimage.feature
from matplotlib import pyplot as plt
from skimage import color
from skimage.feature import hog
from sklearn import svm
from sklearn.metrics import classification_report,accuracy_score
import copy
import os
import pickle

path = r"E:\OMR\cnn_trainingset"
os.chdir(path)

lis = os.listdir(path)
d = pd.DataFrame()
for i in lis:
    f = pd.read_csv(i)
    d = pd.concat([d, f], axis =0)
print(d)

d = d.iloc[1:, 1:]
labs = d.iloc[:, 0]
d = d.iloc[:, 1:]
print(d.head(10))
print(labs.value_counts())

labs = labs.to_numpy()
labs = labs.reshape(-1, 1)
print(labs.shape)

clf = svm.SVC(probability=True)
data_frame = np.hstack((d, labs))
np.random.shuffle(data_frame)

percentage = 80
partition = int(len(labs)*percentage/100)
x_train, x_test = data_frame[:partition,:-1],  data_frame[partition:,:-1]
y_train, y_test = data_frame[:partition,-1:].ravel() , data_frame[partition:,-1:].ravel()

clf.fit(x_train,y_train)

y_pred = clf.predict(x_test)
print("Accuracy: "+str(accuracy_score(y_test, y_pred)))
print('\n')
print(classification_report(y_test, y_pred))

directory = r"E:\OMR"
os.chdir(directory)

with open('cnn_notes_SVM', 'wb') as f:
    pickle.dump(clf, f)
