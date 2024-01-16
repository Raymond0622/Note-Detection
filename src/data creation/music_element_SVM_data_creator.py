import numpy as np
import cv2
import copy
import matplotlib.pyplot as plt
import pandas as pd
import multiprocessing as mp
import pickle
from sklearn import svm
from sklearn.cluster import DBSCAN
import matplotlib.cm as cm
import matplotlib
import os
from pynput import keyboard

path = r"E:\OMR\labelingset_nostaffline_widmung3"
os.chdir(path)

width = 23 # must be odd
ee = width // 2
lis = os.listdir()

labels = []
data = []
for ii in range(1351, 1352):
    l = 0
    img = cv2.imread(lis[ii])
    _rows, _cols, l = img.shape
    print(_rows, _cols, l)
    for i in range(ee, _rows - ee):
        for j in range(ee, _cols - ee):
            imgg = copy.deepcopy(img)
            imgg[i, j] = (255, 0, 0)
            cv2.namedWindow("1", cv2.WINDOW_NORMAL) 
            cv2.resizeWindow("1", 500, 500) 
            cv2.rectangle(imgg,  (j-ee, i-ee), (j+ee, i+ee), 0, 1)
            cv2.imshow('1', imgg)
            cv2.waitKey(3)
            imggg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            datum = imggg[i - ee:i+ee+1, j-ee:j+ee+1].flatten()
            while True:
                with keyboard.Events() as events:
                    event = events.get(1e6)
                # Block for as much 
                    if event.key == keyboard.KeyCode.from_char('1'):
                        print("YES")
                        label = 1
                        l = 0
                        break
                    if event.key == keyboard.KeyCode.from_char('0'):
                        label = 0
                        l = 0
                        break
                    if event.key == keyboard.KeyCode.from_char('q'):
                        l = 1
                        break
                    if event.key == keyboard.KeyCode.from_char('2'):
                        l = 2
                        break
            if l == 1:
                break
            if l == 2:
                break
            labels.append(label)
            data.append(datum)
        print(ii)
        if l == 1:
            break
    ll = pd.DataFrame(labels)
    dd = pd.DataFrame(data)
    DATA = pd.concat([ll, dd], axis = 1)
    DATA.to_csv('cnn_data_widmung3_3_notes.csv')
