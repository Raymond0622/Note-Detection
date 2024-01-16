import numpy as np
import cv2
import pandas as pd
import os
import time
import shutil

start = time.time()

f = open('staff_height.txt', 'r')
STAFF_HEIGHT = int(f.readline())

# read sheet music without staff line
img = cv2.imread("first_step.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_rows, _cols = img_gray.shape

# Read the csv that contain location of each pixel of each music element respect to the original sheet music

df = pd.read_csv("second_step.csv", header=None)
df = df.rename(columns={0: "y", 1: "x", 2: "label"})

# Group by the DBSCAN clusters by its label and find the max and min of pixel location of each music element
MAX = df.groupby(['label']).max()
MIN = df.groupby(['label']).min()
TOT = pd.concat([MAX, MIN], axis = 1)

ll = int(len(MAX))
zz = pd.Series(np.zeros((ll))).astype(int)
rr = (_rows-1)*pd.Series(np.ones((ll))).astype(int)
cc = (_cols-1)*pd.Series(np.ones((ll))).astype(int)

# Saturation to prevent minimum, maxmimum pixel location that is outside the range of original sheet music pixel
MIN_y = np.maximum(TOT.iloc[:, 2] - 5, zz).astype(int)
MIN_x = np.maximum(TOT.iloc[:, 3] - 5, zz).astype(int)
MAX_y = np.minimum(TOT.iloc[:, 0] + 5, rr).astype(int)
MAX_x = np.minimum(TOT.iloc[:, 1] + 5, cc).astype(int)

# remove entire folder before new music element to be created
shutil.rmtree("/Volumes/ESD-USB/OMR/music_parts")

# create folder for music elements
os.mkdir('music_parts')

directory = r"/Volumes/ESD-USB/OMR/music_parts"
os.chdir(directory)
dfd = pd.DataFrame(columns = ['x', 'y'])
dfdd = pd.DataFrame(columns = ['x', 'y'])


# define minimum area of a music element. If it's smaller, we skip analyzing.
min_Area = STAFF_HEIGHT * STAFF_HEIGHT

for i in range(len(MAX)):
    area = (MAX_y[i] - MIN_y[i]) * (MAX_x[i] - MIN_x[i])
    t = 0
    if area < min_Area:
        continue
    # The below code prevents music element to be repeatedly analyzed by finding elements
    # that are contained by another element
    for j in range(len(MAX)):
        if (j != i):
            if ((MAX_x[i] <= MAX_x[j]) and (MIN_x[i] >= MIN_x[j])):
                if ((MAX_y[i] <= MAX_y[j]) and (MIN_y[i] >= MIN_y[j])):
                    t = 1
                    break
    # If it passes all criteria (not contained by another element, or at least size of minimum area), then
    # we create the music element. This step is to prevent predicting pixels of elements that are already
    # repeated or will not contain any note heads. 
                
    if t == 0:
        string = 'musicpart_nostaffline' + str(i) + '.jpg'
        dfd = pd.concat([dfd, pd.DataFrame([[MAX_x[i], MAX_y[i]]], columns = ['x', 'y'])])
        dfdd = pd.concat([dfdd, pd.DataFrame([[MIN_x[i], MIN_y[i]]], columns = ['x', 'y'])])
        cv2.imwrite(string, img[MIN_y[i]:MAX_y[i] + 1, MIN_x[i]:MAX_x[i] + 1])


# create csv files that contain the pixel location of each music element. Max, min values
# corresponds to southeast, northwest corner the music element box. 
        
directory = r"/Volumes/ESD-USB/OMR/"
os.chdir(directory)
dfd.to_csv('third_step_xy_max.csv', index=False, header=True)
dfdd.to_csv('third_step_xy_min.csv', index=False, header=True)
end = time.time()
print('third_step:', end-start)
 