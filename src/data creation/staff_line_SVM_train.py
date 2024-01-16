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

directory = r"/Volumes/ESD-USB/OMR/splitset"
os.chdir(directory)

d = pd.read_csv('data.csv')
df = d.values
#print(df[0])
lab = pd.read_csv('labels.csv')
labs = lab.iloc[:, 0]
print(lab.value_counts())

labs = labs.to_numpy()
labs = labs.reshape(-1, 1)
print(labs.shape)

clf = svm.SVC()
data_frame = np.hstack((df, labs))
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

directory = r"/Volumes/ESD-USB/OMR/"
os.chdir(directory)

with open('start_line_SVM', 'wb') as f:
    pickle.dump(clf, f)

img = cv2.imread('0010.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_rows, _cols = img_gray.shape
fact = 1600/_rows
img = cv2.resize(img, (int(_cols * fact), 1600),  interpolation = cv2.INTER_LINEAR)
img_color = copy.deepcopy(img)
img_gray = cv2.resize(img_gray, (int(_cols * fact), 1600),  interpolation = cv2.INTER_LINEAR)
_rows, _cols = img_gray.shape

count = 0
for j in range(_cols):
    img_g = copy.deepcopy(img_gray)
    row = img_gray[:, j]
    g = clf.predict(row.reshape(1, -1))
    if g == 1 and count == 5:
        for i in range(begin, j):
            img = cv2.line(img, (i, 0), (i, _rows), (0, 0, 255), 1)
        count = 0
        break
    elif g == 1 and count != 5:
        begin = j
        count = count + 1
    else:
        count = 0

cv2.line(img_g, (j, 0), (j, _rows), 0, 1)
cv2.imshow('1', img_g)
cv2.imshow('image', img)
cv2.waitKey(0)

_x = begin
count = 0
cons = []
loca = [0]

for i in range(len(row)):
    if (255 - row[i]) < 20:
        count = count + 1
    else:
        cons.append(count)
        loca.append(int(i))
        count = 0
(n, bins, patches) = plt.hist(cons)
print(bins)
print(n)
print(loca)
plt.show()
consP = pd.Series(cons)
s = consP.value_counts().index.to_list()
print('s', s)
# try K-means. It's simple and quick
# select first two points as the cluster points

c1 = s[0]
c2 = s[1]
c10 = -1
c20 = -1
iter = 0
while (c1 != c10 or c2 != c20) and iter < 50:
    c10 = c1
    c20 = c2
    first = []
    second = []
    for i in s:
        g = np.array([(i - c10)**2, (i - c20)**2])
        X = np.argmin(g)
        if X == 0:
            first.append(i)
            print(1,  i)
        else:
            second.append(i)
            print(2, i)
    c1 = np.mean(np.array(first))
    c2 = np.mean(np.array(second))
    iter = iter + 1

C = max(c1, c2)
if C == c2:
    store = second
else:
    store = first
ans = []
loca.append(_rows)
for i in range(len(cons)):
    if cons[i] in store:
        ans.append(int((loca[i] + loca[i + 1])/2))
for j in ans:
    cv2.line(img, (0, j), (_cols, j), (255, 0, 0), 2)

cv2.namedWindow("e", cv2.WINDOW_NORMAL)
# Using resizeWindow()
cv2.resizeWindow("e", 700, 200)
cv2.imshow('e', img)
cv2.waitKey(0)
ans.append(_rows)

## staff removal 

no_staff = [filename for filename in os.listdir(r"/Volumes/ESD-USB/OMR/imageset") if filename.startswith("non_staff_line")]
yes_staff =  [filename for filename in os.listdir(r"/Volumes/ESD-USB/OMR/imageset") if filename.startswith("staff_line")]

numNO = len(no_staff)
numYES = len(yes_staff)
TOT = numNO + numYES
print('number of no :', numNO)
print('number of yes :' , numYES)


directory = r"/Volumes/ESD-USB/OMR/imageset"
os.chdir(directory)

sam = cv2.imread('non_staff_line0.jpg')
sam_gray = cv2.cvtColor(sam, cv2.COLOR_BGR2GRAY)
_rows, _cols = sam_gray.shape

IM = np.zeros((TOT, _rows*_cols))

for i in range(len(no_staff)):
    G = cv2.imread(no_staff[i])
    G = cv2.cvtColor(G, cv2.COLOR_BGR2GRAY)
    G = G.flatten()
    IM[i, :] = G

for i in range(numYES):
    G = cv2.imread(yes_staff[i])
    G = cv2.cvtColor(G, cv2.COLOR_BGR2GRAY)
    G = G.flatten()
    IM[i + numNO, :] = G

print('shape of image matrix: ', IM.shape)
nos = np.zeros((len(no_staff), 1))

yes_staff = [filename for filename in os.listdir(r"/Volumes/ESD-USB/OMR/imageset") if filename.startswith("staff_line")]
yes = np.ones((len(yes_staff), 1))

y = np.vstack((nos, yes))
print('answer shape:', y.shape)

clf = svm.SVC()
data_frame = np.hstack((IM, y))
np.random.shuffle(data_frame)

percentage = 80
partition = int(TOT*percentage/100)
x_train, x_test = data_frame[:partition,:-1],  data_frame[partition:,:-1]
y_train, y_test = data_frame[:partition,-1:].ravel() , data_frame[partition:,-1:].ravel()

clf.fit(x_train,y_train)

directory = r"/Volumes/ESD-USB/OMR/"
os.chdir(directory)

with open('staff_removal_SVM', 'wb') as f:
    pickle.dump(clf, f)

y_pred = clf.predict(x_test)
print("Accuracy: "+str(accuracy_score(y_test, y_pred)))
print('\n')
print(classification_report(y_test, y_pred))

#ans.insert(0, 0)

#directory = r"C:\Users\Raymond Park\Desktop\OMR\brahms_violin_concerto"
#os.chdir(directory)

cv2.imshow('1', img_gray)
cv2.waitKey(0)

for ii in range(1, len(ans)):
    win = 4

    score = img_color[ans[ii - 1] + 7:ans[ii] - 7, :]
    _rows, _cols, _c = score.shape
    
    score_copy = copy.deepcopy(score)
    score_copy1 = copy.deepcopy(score)
    score_gray = cv2.cvtColor(score, cv2.COLOR_BGR2GRAY)
    score_line = cv2.Canny(score_gray, 50, 150)
    print(score_line.shape)
    _rows, _cols = score_gray.shape
    #cv2.imshow('1', score_gray)
    #cv2.waitKey(0)

    for x in range(win, _cols - win):
        for y in range(win, _rows - win):
            box_line = score_line[y - win: y + win, x - win: x + win + 1]
            #box_line = score_gray[y0 + z - win:y0 + z + win, x0 + t - win:x0 + t + win + 1]
            #cv2.imshow('e', box_line)
            #cv2.waitKey(0)
            fd = box_line.flatten()
            g = clf.predict(fd.reshape(1, -1))
            if g == 1:
                score_gray[y, x] = 255
        cv2.rectangle(score, (x - win, y - win), (x + win + 1, y + win + 1), (0, 0, 255), 2)
            
        #cv2.imshow('e', score_gray)
        #cv2.waitKey(0)
        #cv2.imshow('s', score_line)
        #cv2.waitKey(0)
    img_gray[ans[ii - 1]+7:ans[ii]-7, :]  = score_gray
    #cv2.imshow('1', score)
    #cv2.imshow('org', score_copy)
    #cv2.imshow('e', score_gray)
    #cv2.waitKey(0)

directory = r"/Volumes/ESD-USB/OMR/"
os.chdir(directory)

cv2.imshow('final', img_gray)
cv2.waitKey(0)
cv2.imwrite('naive_staff.jpg', img_gray)