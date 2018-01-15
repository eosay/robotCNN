# robotCNN
Supervised learning with a Convolutional Neural Network to control a linear robotic slider with hand gestures. The CNN is trained and used for inference on a PC, with movement commands sent over USB serial communication to a microcontoller. The CNN classifies webcamera images for the classes 'left', 'right', and 'stop'. The network is built and trained using [Pytorch](http://pytorch.org/). A GPU is highly recommended, but CPU usage is also supported. The blog post for this project is [here](https://cascino.github.io/Abstract-Robotic-Control-with-Convolutional-Neural-Networks/).
<p align="center", text-align="center">
  <img src="/images/infer.gif" width="450"><br>
  Neural Network inference on pointing hand gestures
</p>

## Prerequisites
```
Python3
pytorch
torchvision
cv2
pyserial
```

### Hardware
* [Pyboard](https://store.micropython.org/) - or other microcontroller running [Micropython](https://micropython.org/)
* Bipolar Stepper Motor
* [A4988 Stepper Motor Driver](https://www.pololu.com/product/1182)
* Resistors, capacitors, limit switches
* Power Supply for stepper motor

## Usage
Collect data from webcamera.
```
python3 collect.py
```
Once collect.py is run three times for seperate data classes, the network can be trained.
```
python3 train.py
```
Now run the network for live inference and robotic control. This command may need to be run as root, since it deals with USB serial communication.
```
python3 infer.py
```




