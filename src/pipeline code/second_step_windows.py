import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN
import sys
import time

start = time.time()

image_file_name = sys.argv[1]

img = cv2.imread(image_file_name)
img_gray_final = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_rows, _cols = img_gray_final.shape
X = []

# Find where pixels are greater than 200, essentially that is nonzero since
# we turned each pixel to 0 or 255 from 1st step
# Each dark pixel will then clustered based on distance between 
# dark pixels, etc.

imggg = np.where((np.int16(img_gray_final) - 200) > 0, 1, 0)
for gg in range(_rows):
    for ggg in range(_cols):
        if imggg[gg, ggg] == 0:
            X.append([gg, ggg])

# DBSCAN clustering, the parameters listed below were the parameters with best performance
X = np.array(X)
clustering = DBSCAN(eps=2, min_samples=1).fit(X)
labels = clustering.labels_
labels = np.array(labels).reshape(-1, 1)
K = np.hstack((X, labels))
G = pd.DataFrame(K)

# Create csv that contains the location of each pixel along with the labels
G.to_csv('second_step.csv', index=False, header=False)

end = time.time()
print('second_step:', end-start)

# Create a colorful image of the clusters (again optional)
P = len(labels)
colors = np.random.rand(P, 3)
plt.scatter(X[:, 1], -X[:, 0], s=0.5, c=colors[labels])
plt.savefig('DBSCAN.png')
