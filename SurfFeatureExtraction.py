import json
import numpy as np
import cv2
from os import listdir
import pickle

surf = cv2.xfeatures2d.SURF_create(300, 6)

wikidata_files = listdir('./wikidata/')

i = 0

for wikidata_file in wikidata_files:
    if wikidata_file.endswith('.jpg'):
        img1 = cv2.imread('./wikidata/' + wikidata_file, 0)  # queryImage
        height, width = img1.shape
        larger = height if height > width else width
        if larger > 1500:
            ratio = 1500.0 / larger
            img1 = cv2.resize(img1, (0, 0), fx=ratio, fy=ratio)
            # img1 = cv2.equalizeHist(img1)
        kp1, des1 = surf.detectAndCompute(img1, None)
        with open('./wikidata/' + wikidata_file + '.surf', 'wb') as surf_feature_file:
            pickle.dump(des1, surf_feature_file)
        print(str(i) + ' ' + wikidata_file)
        i += 1
