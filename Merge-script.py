import cv2
import numpy as np
from pathlib import Path
import sys

# Extracting coordinates
positions = []
POS_PATH = 'img-global-positions-0.txt'
with open(POS_PATH) as f:
    lines = f.readlines()
    for line in lines:
        #print(line)
        words = line.split()
        pos = (int(words[5][1:-1]), int(words[6][:-2]))
        #print(pos)
        positions.append(pos)

slide = str(sys.argv[1])
IMGS_PATH = Path(slide)
imgs = sorted(list(IMGS_PATH.glob('*')))
#print(imgs)
#print(len(imgs), len(positions))

img = cv2.imread(str(imgs[0]))
h, w = img.shape[:2]
#print(w, h)

W = 0
H = 0
for i in range(len(positions)):
    x = positions[i][0]
    if x > W:
        W = x
    y = positions[i][1]
    if y > H:
        H = y
W += w
H += h
#print(W, H)

ground = np.zeros((H, W, 3), dtype=np.uint8)

print("Merging images...")
for i in range(len(imgs)):
    img = cv2.imread(str(imgs[i]))
    x = positions[i][0]
    y = positions[i][1]
    #print(x, y)
    for row in range(h):
        ground[row+y][x:x+w] = img[row]

print("Saving...")
cv2.imwrite(slide + '.png', ground)
