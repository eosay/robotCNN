import torch
from model import CNN, ImgDataset
from torch.autograd import Variable
from torch import nn, optim

use_cuda = torch.cuda.is_available()

# hyperparameters
batch_size = 64
lr = 0.001
epochs = 5

data = ImgDataset(batch_size=batch_size)
dataloader = data.dataloader

net = CNN()
net.train()

if use_cuda:
    print('CUDA device found, now active')
    net.cuda()

crit = nn.CrossEntropyLoss(size_average=False)
optimizer = optim.SGD(net.parameters(), lr, weight_decay=0.0001)

# training loop
for i in range(epochs):
    for j, (data, label) in enumerate(dataloader):
        
        label = Variable(label, requires_grad=False)
        data = Variable(data, requires_grad=False)

        if use_cuda:
            label = label.cuda()
            data = data.cuda()
        
        optimizer.zero_grad()
        pred = net(data)
        loss = crit(pred, label)
        loss.backward()
        optimizer.step()

        print('epoch [{}/{}]    batch [{}]    loss {:.5f}'.format(i, epochs, j, loss.data[0]))

torch.save(net, 'model.pt')


    

    
    
