import torch
from torch import nn
from torch.nn import functional as F 
import torchvision.datasets as dset
import torchvision.transforms as transforms

# dataset class for Pytorch ImageFolder
class ImgDataset():
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.dataset = dset.ImageFolder('./data', transform=transforms.Compose([
                            transforms.ToTensor(), 
                            transforms.Normalize((0.5, 0.5, 0.5),(0.5, 0.5, 0.5))]))

        self.dataloader = torch.utils.data.DataLoader(self.dataset, self.batch_size, shuffle=True, num_workers=2)

# simple Convolutional Neural Network
# 64 x 64 rgb input image -> 3 classes
# {'left': 0, 'right': 1, 'stop': 2}
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 8, 6, 1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(8, 16, 6, 1)
        self.conv3 = nn.Conv2d(16, 24, 6, 1)
        self.fc1 = nn.Linear(24 * 3 * 3, 100)
        self.fc2 = nn.Linear(100, 32)
        self.fc3 = nn.Linear(32, 3)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 24 * 3 * 3)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return x
    