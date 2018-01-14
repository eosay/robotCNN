import numpy as np
import cv2
import os

# sub folder name
save_dir = input('[webcam data collector ready]\nsave directory path: ')
# image prefix that will be indexed
file_name = input('file prefix: ')
im_num = int(input('image number: '))
input('press enter to begin data collection...')

if not os.path.exists(os.path.join('./data', save_dir)):
    os.makedirs(os.path.join('./data', save_dir))

# the camera device, may need to change the device number
cam = cv2.VideoCapture(0)

# gather the data
for i in range(im_num):
    _, im = cam.read()
    # make the image square and resize
    im = im[:, 80:560]
    cv2.imshow('image', im)
    im = cv2.resize(im, (64, 64), interpolation=cv2.INTER_CUBIC)
    path = os.path.join('./data', save_dir, file_name + str(i).zfill(3) + '.jpg')
    print('saved: ',path)
    cv2.imwrite(path, im)
    # show window for 25 ms
    cv2.waitKey(25)

cam.release()
cv2.destroyAllWindows()

