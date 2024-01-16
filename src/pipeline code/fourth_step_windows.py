import cv2
import pandas as pd # linear algebra
import os
import time
import sys

start = time.time()
df = pd.read_csv("third_step_xy_min.csv")
df_max = pd.read_csv("third_step_xy_max.csv")

image_file_name = sys.argv[1]
path = sys.argv[2]
os.chdir(path)

final_image = cv2.imread(image_file_name)
_rows, _cols, l = final_image.shape

final_image = cv2.resize(final_image, (1600, 2150), interpolation=cv2.INTER_LINEAR)
os.chdir(r"/Volumes/ESD-USB/OMR/")

# change path to music parts folder
path = r"/Volumes/ESD-USB/OMR/music_parts"
os.chdir(path)

lis = os.listdir()

# Create bounding box of each music element on the original sheet music

for i in range(len(lis)):

    x = int(df.loc[i].x)
    y = int(df.loc[i].y)

    x2 = int(df_max.loc[i].x)
    y2 = int(df_max.loc[i].y)

    cv2.rectangle(final_image, (x, y), (x2, y2), (0, 0, 255), 2)

path = r"/Volumes/ESD-USB/OMR/"
os.chdir(path)
cv2.imwrite('music_parts_box.jpg', final_image)

end = time.time()
print('fourth_step:', end-start)

