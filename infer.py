import torch
import cv2
import numpy as np
import serial
import torchvision.transforms as transforms
from torch.autograd import Variable
from torch.nn import functional as F 

# camera device, may need to change the device number
cam = cv2.VideoCapture(0)
use_cuda = torch.cuda.is_available()

img_transforms = transforms.Compose([
    transforms.ToTensor(),    
    transforms.Normalize((0.5, 0.5, 0.5),(0.5, 0.5, 0.5)),
])

def get_frame():
    _, frame = cam.read()
    # make image a square and resize
    frame = frame[:, 80:560]
    
    cv2.imshow('image', frame)
    # show frame for 50 ms
    cv2.waitKey(50)

    frame = cv2.resize(frame, (64, 64), interpolation=cv2.INTER_CUBIC)
    frame = frame.astype(np.float32)
    # apply image transforms to normalize...
    im = img_transforms(frame).unsqueeze_(0)

    return im

model = torch.load('model.pt')
model.eval()
if use_cuda:
    print('CUDA device found, now active')
    model.cuda()

# open a serial connection to the pyboard
# may need to change the device connection string
ser = serial.Serial('/dev/ttyACM0')

# continuously run the network for inference
while True:
    # get a frame and feed it through the net
    capture = get_frame()
    x = Variable(capture)

    # apply softmax to net output, since CrossEntropy loss is not being used, 
    # (Pytorch CrossEntropyLoss already includes log_softmax)
    if use_cuda:
        x = x.cuda()
        x = F.softmax(model(x)).cuda()
        x = x.data.cpu().numpy()[0]
    else:
        x = F.softmax(model(x))
        x = x.data.numpy()[0]
    
    print(x)  
    # get the most confident classification
    x_max = np.argmax(x)

    # send bits over serial connection for direction/enable instructions
    # {stop} classification sends nothing
    if x_max == 0:
        print('left')
        ser.write(b'10')
    elif x_max == 1:
        print('right')
        ser.write(b'01')
    else:
        print('stop')

cam.release()
cv2.destroyAllWindows()
