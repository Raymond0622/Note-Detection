import cv2
import numpy as np
import os
import keyboard
from pynput import keyboard
import time
from fractions import Fraction
import copy
import matplotlib.pyplot as plt
import random
import math
import pandas as pd

# where to start
where = 0
view = 30
def Show(img):
    plt.imshow(img)
    plt.show()

win = 4
startY = [-win - 1]
endY = [-win - 1]

score = cv2.imread("sample9.jpg")
_rows, _cols, _c = score.shape
fact = 1600/_cols
score = cv2.resize(score, (1600, int(fact*_rows)),  interpolation = cv2.INTER_LINEAR)
score_gray = cv2.cvtColor(score, cv2.COLOR_BGR2GRAY)
score_line = cv2.Canny(score_gray, 50, 150)
_rows, _cols = score_gray.shape

staff = 609
non_staff = 1203

directory = r"C:\Users\Raymond Park\Desktop\OMR\imageset"
os.chdir(directory)
score_copy = copy.deepcopy(score)
for s in range(5):
    Found = True
    i = 0
    yy = startY[s] + win + 1
    yyy = endY[s] + win + 1
    while (Found):
        d = score_line[yy:, i]
        if np.mean(d) != 0:
            Found = False
        else:
            i = i + 1
    x0 = i + 1
    y0 = np.argmax(score_line[yy:, x0] > 0) + yy
    print(y0)
    Show(score_line)
    Edge = True
    k = _cols - 1
    while (Edge):
        d = score_line[yyy:, k]
        if np.mean(d) != 0:
            Edge = False
        else:
            k = k - 1
    x1 = k - 7
    startY.append(y0)
    if s != 0:
        y1 = max(np.argmax(score_line[yyy:, x1] > 0) + yyy, startY[s + 1] - startY[s] + endY[s])
    else:
        y1 = np.argmax(score_line[yyy:, x1] > 0) + yyy
    print("y1", np.argmax(score_line[yyy:, x1] > 0) + yyy)
    print("end", endY)
    print("start", startY)
    print(x0, y0, x1, y1)

    endY.append(y1)

    dx = x1 - x0
    dy = y0 - y1
    changeX = dx//dy
    if dy == 0:
        changeX = x1 - x0 + 1
    y0 = y0 + 1
    # skipping

    if s < where:
        continue
    for t in range(win, x1 - x0 + 1):
        if (t % changeX) == 0:
                y0 = y0 - 1
        for e in range(-3, 3):
            #print(changeX, dy, dx)
            #print(k % changeX)
            

            box_line = score_line[y0 - win + e:y0 + win + e, x0 + t - win:x0 + t + win + 1]
            score_line_color = cv2.cvtColor(score_line,cv2.COLOR_GRAY2RGB)
            score_line_color[y0 + e, x0 + t] = (255, 0, 0)
            box_line_color = score_line_color[y0 - win + e:y0 + win + e, x0 + t - win:x0 + t + win + 1]
            print('bb', box_line.shape)
            score_copy = copy.deepcopy(score)
            score_copy[y0 + e, x0 + t, :] = (255, 0, 0)
            box = score_copy[y0 - win + e:y0 + win + e, x0 + t - win:x0 + t + win + 1]
            
            cv2.namedWindow("box_line", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("box_line", 500, 500)
            cv2.imshow('box_line', box_line)

            cv2.namedWindow("box_color", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("box_color", 500, 500)
            cv2.imshow('box_color', box)
            cv2.namedWindow("box_line_color", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("box_line_color", 500, 500)
            cv2.imshow('box_line_color', box_line_color)
         

            # For viewing the imageset respect to where on the score
            score_copy = copy.deepcopy(score)
            cv2.namedWindow("viewing window", cv2.WINDOW_NORMAL)

            cv2.resizeWindow("viewing window", 500, 500)
            score_copy[y0 + e, x0 + t] = (255, 0, 0)
            img = score_copy[y0 + e - win - view:y0 + e + win + view + 1, x0 + t - win:x0 + t + 2*view + 2*win + 2]
            cv2.rectangle(score_copy, (x0 + t - win, y0 - win + e), (x0 + t + win, y0 + win + e), (0, 0, 255), 1)
            cv2.imshow('viewing window', img)
            cv2.waitKey(0)

            while True:
                with keyboard.Events() as events:
                    # Block for as much as possible
                    event = events.get(1e6)
                    if event.key == keyboard.KeyCode.from_char('1'):
                        print("YES")
                        filename_line = "staff_line" + str(staff) + ".jpg"
                        filename_img = "staff_color" + str(staff) + ".jpg"
                        staff = staff + 1
                        break
                    if event.key == keyboard.KeyCode.from_char('0'):
                        filename_line = "non_staff_line" + str(non_staff) + ".jpg"
                        filename_img = "non_staff_color" + str(non_staff) + ".jpg"
                        non_staff = non_staff + 1
                        break
            time.sleep(0.1)
            cv2.imwrite(filename_line, box_line)
            cv2.imwrite(filename_img, box)