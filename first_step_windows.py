import numpy as np
import cv2
import copy
import sys
import pandas as pd
import multiprocessing as mp
import pickle
import time
import subprocess
import os


def PREDICT(where, XX):
    N = []
    Q = []
    start = int(where[0])
    end = int(where[1])
    for i in range(start, end + 1):
        iii = XX[i]
        _y = int(iii // _COLS)
        _x = int(iii % _COLS)
        for ee in range(-STAFF_REM_HEIGHT, STAFF_REM_HEIGHT+1):

            # For each staff line pixel belonging to a shortest path, we
            # go through pixels that's STAFF_REM_HEIGHT pixels away from the main staff line pixel
            # and create a image box that is of size 8 x 9 pixel to be fed into SVM

            box_line = score_line[_y + ee - win:_y + ee + win, _x - win:_x + win + 1]
            fd = box_line.ravel().tolist()
            if (len(fd) == 72):
                N.append(fd)
                Q.append([_y + ee, _x])

    # WE stack each box to be predicted into a tensor to be all predicted at once
    # This is much quicker than calling the prediction function on each individual box
    N = np.array(N)
    
    L = mod.predict(N)
    L = np.array(L).reshape(-1, 1)
    Q = np.array(Q)
    L = np.hstack((L, Q))
    return L
    
s = sys.argv[2]
os.chdir(s)
start = time.time()

# Number of multiprocesses is one less than the number of cpus on a computer. This can change
POOL_COUNT = mp.cpu_count() - 1
results = []
image_file_name = sys.argv[1:2][0]
print(image_file_name)

img = cv2.imread(image_file_name)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Change size of image to 2150 x 1600 pixels

img_gray = cv2.resize(img_gray, (1600, 2150), interpolation=cv2.INTER_LINEAR)
img_color = cv2.resize(img, (1600, 2150), interpolation=cv2.INTER_LINEAR)
img_grayDF = pd.DataFrame(img_gray)

# Change this to whichever directory all OMR files are located at
os.chdir(r"/Volumes/ESD-USB/OMR/")

# Converting gray-ed image's pixel value to a text
img_grayDF.to_csv('trial.txt', index=None, header=None)
_ROWS, _COLS = img_gray.shape
_rows, _cols = img_gray.shape

# Perform Canny edge detection to be fed into SVM
img_gray_final = copy.deepcopy(img_gray)
score_line = cv2.Canny(img_gray.astype(np.uint8), 50, 150)

# This is an important step. We strictly want either 0, 255 pixel for our shortest path algorthim to work properly
img_gray = 255 * np.where((np.int16(img_gray) - 200) > 0, 1, 0)

img_gray_org = copy.deepcopy(img_gray)
backtorgb = cv2.cvtColor(img_gray.astype(np.uint8), cv2.COLOR_GRAY2RGB)

# Determining staff height (or the space between staff lines)
white = []
for i in range(_cols):
    ROW = img_gray[:, i]
    white_p = 0
    for j in range(_rows):
        if (ROW[j]- 200) > 0:
            white_p = white_p + 1
        else:
            if white_p != 0:
                white.append(white_p)
                white_p = 0

# Essentially get the more common runs of white pixels for each column of the image
STAFF_HEIGHT = pd.Series(white).value_counts().index.to_list()[0]
GG = 1
win = 4
STAFF_REM_HEIGHT = STAFF_HEIGHT // 3

# write staff height to a file as it is an important paramater for rest of the procedure
f = open('staff_height.txt', 'w')
f.write(str(STAFF_HEIGHT))
f.close()

# load staff removal SVM model
with open('staff_removal_SVM', 'rb') as f:
    mod = pickle.load(f)

if __name__ == '__main__':

    # Call shortest path algorthim
    subprocess.call(["gcc", "minHeap_Shortest_Path.c"]) 
    tmp=subprocess.call("./a.out")

    # list all paths in outX.txt file for multiple out files in case we used fork()

    prefixed = [filename for filename in os.listdir('.') if filename.startswith("out")]

    # Create a blank sheet music, same size as that of the original sheet music to portray
    # just staff lines

    G = 255*np.ones((_rows, _cols))
    for j in prefixed:
        if (os.path.getsize(j) != 0):
            L = pd.read_csv(j, header=None).to_numpy()
            X = L[0]
            for i in range(len(L[0]) - 1):
                x = int(X[i] % _cols)
                y = int(X[i] / _cols)
                G[y, x] = 0
    G = G.astype(np.uint8)

    # Find which pixels are staff line pixel to be fed into SVM
    XX = np.where(G.flatten() == 0)[0]

    # Separate the pixels into equal bags to be multiprocessed for speedup
    f = []
    num = len(XX) / POOL_COUNT
    rem = len(XX) % POOL_COUNT
    for i in range(POOL_COUNT):
        f.append(([i*num, (i + 1)*num - 1], XX))
        start = time.time()

    # Predicting if a pixel belongs to staff line or not
    with mp.Pool(POOL_COUNT) as p:
        results = p.starmap(PREDICT, f) 
    
    # For each process, if the prediction is staff line, then we turn the pixel into a white pixel
    # The output of mp.Pool is a 3D tensor
    for j in range(POOL_COUNT):
        for i in range(len(results[j])):
            if results[j][i][0] == 1:
                img_gray_final[int(results[j][i][1]), int(results[j][i][2])] = 255
    
    # "staff_lines.jpg" is the only staff line image
    # "first_step,jpg" is the sheet music with staff lines removed
                
    cv2.imwrite('staff_lines.jpg', G)
    cv2.imwrite('first_step.jpg', img_gray_final)    
    end = time.time()
    print('first_step:', end-start)
    
    
