import numpy as np
import cv2
import pandas as pd 
import copy
import multiprocessing as mp
import os
import pickle
import math
import matlab.engine
import time
import sys

# Euclidean distance function in 2D
def dist(x, y, x1, y1):
    d = ((x - x1)**2 + (y - y1)**2)**0.5
    return d

# Main function DB which takes input argument ar, num.
# ar - contains the start and end index of the music elements to be analyzed per multiprocessing pool
# num is the index of the pool to create individual csv files, etc.
def DB(ar, num):
    store = [[-100, -100]]
    start = int(ar[0])
    end = int(ar[1])

    for ii in range(start, end):

        path = r"/Volumes/ESD-USB/OMR/music_parts"
        os.chdir(path)
        img = cv2.imread(lis[ii])
        _rows, _cols, l = img.shape

        prob = np.zeros((_rows, _cols))
        target = 0
        W = []
        Q = []

        # Create boxes to be fed into prediction (its a 11 x 11 pixel)
        # Again, create all boxes at once and feed it into the model
        for i in range(ee, _rows - ee):
            for j in range(ee, _cols - ee):
                imgg = copy.deepcopy(img)
                imgg[i, j] = (255, 0, 0)       
                imggg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                datum = imggg[i - ee:i+ee+1, j-ee:j+ee+1].flatten().tolist()
                W.append(datum)
                Q.append([i, j])
                target = 1
        # Find probability that a center pixel of 11 x 11 pixel is part of note head
        # We desire to find the center pixel of a note head. So you, some sort of 
        # discretized version of gradient descent method to find the center pixel since
        # it's likely that the center pixel will have the highest probability to be a note head
                
        if target == 1:
            lab = model.predict_proba(np.array(W))
        
            for i in range(len(W)):
                # Required log function to find the maximum probability
                prob[Q[i][0], Q[i][1]] = math.log(1 - lab[i][1])

            df = pd.DataFrame(prob)

            path = r"/Volumes/ESD-USB/OMR/"
            os.chdir(path)
            fi = 'probtest' + str(num) + '.csv'
            df.to_csv(fi, index=False, header=False)
            diffx = dff.loc[ii, :].x
            diffy = dff.loc[ii, :].y

            # Feed the converted probability to MATLAB function for gradient descent procedure
            # This could have been done on Python or C, but wanted to use matlab engine and see
            # what it's like 

            res = eng.OMR_Function(fi, num)#nargout=0)

            # If a note head is detected (i.e the GD procedure fixes onto a single point), then
            # returns the location of the note head respect to the music element, not the original
            # sheet music. Therefore, we required to use of diffx, diffy variable which contain the
            # the location the music element's top left corner. 

            if res == 1:
                fi = 'notes_position' + str(num) + '.csv'
                rr = pd.read_csv(fi, header=None)
                
                QQ = len(store)
                for jj in range(len(rr)):
                    for qq in range(QQ):
                        Q = rr.loc[jj, :]
                        x = Q[0]
                        y = Q[1]
                        # Prevents center pixels to be too closely together
                        if dist(x + diffx, y + diffy, store[qq][0], store[qq][1]) < 10:
                            break
                    store.append([x + diffx, y + diffy])
    return store

# training width (this is fixed as per how the SVM model was trained)
width = 23
ee = width // 2

# Number of multiprocessing pools to be one less than the number of cpus
POOL_COUNT = mp.cpu_count() - 1
path = r"/Volumes/ESD-USB/OMR/"
os.chdir(path)

# start matlab engine
eng = matlab.engine.start_matlab()

# load SVM model for detecting note heads
model = pickle.load(open('cnn_notes_SVM' , 'rb'))
dff = pd.read_csv("third_step_xy_min.csv")

# Listing out the music elements to be analyzed
path = r"/Volumes/ESD-USB/OMR/music_parts"
os.chdir(path)
lis = os.listdir()


if __name__ == '__main__':

    # Distributing the music elements to each pool equally
    start = time.time()
    f = []
    num = len(lis) // POOL_COUNT 
    rem = len(lis) % POOL_COUNT

    for i in range(POOL_COUNT):
        f.append(([i*num, (i + 1)*num], i))

    with mp.Pool(POOL_COUNT) as p:
        store = p.starmap(DB, f)

    s = sys.argv[2]
    os.chdir(s)

    # Read image of original sheet music to annotate bounding boxes
    image_file_name = sys.argv[1]
    final_image = cv2.imread(image_file_name)
    _rows, _cols, l = final_image.shape
 
    final_image = cv2.resize(final_image, (1600, 2150), interpolation=cv2.INTER_LINEAR)
    num = 0

    # Create bounding box around each detected note head from output of multiprocessing pools
    for j in range(POOL_COUNT):
        for i in range(1, len(store[j])):
            x = int(store[j][i][0])
            y = int(store[j][i][1])

            # STAFF_HEIGHT was around 12-14. Therefore, the bounding box/square should be around theat width
            cv2.rectangle(final_image, (x - 7, y- 7), (x + 7, y + 7), (0, 0, 255), 2)
            # Find the number of note heads detected
            num = num + 1
    
    when = sys.argv[3]
    cv2.imwrite('FINAL' + str(when) + '.jpg', final_image)
    end = time.time()
    print('fifth_step:', end-start)

    # Save number of "notes" per page
    f = open('num_notes.txt', 'a')
    f.write(str(num) + "\n")
    f.close()
    


