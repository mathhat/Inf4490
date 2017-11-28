#!/usr/bin/env Python3
'''
    This file will read in data and start your mlp network.
    You can leave this file mostly untouched and do your
    mlp implementation in mlp.py.
'''
# Feel free to use numpy in your MLP if you like to.
import numpy as np
import mlp

filename = '../data/movements_day1-3.dat'

movements = np.loadtxt(filename,delimiter='\t')
#for i in range(8*18):
#    print (sum(movements[i,0:39]) , "   ", movements[i,-1])

# Subtract arithmetic mean for each sensor. We only care about how it varies:
movements[:,:40] = movements[:,:40] - movements[:,:40].mean(axis=0)

# Find maximum absolute value:
imax = np.concatenate(  ( movements.max(axis=0) * np.ones((1,41)) ,
                          np.abs( movements.min(axis=0) * np.ones((1,41)) ) ),
                          axis=0 ).max(axis=0)

# Divide by imax, values should now be between -1,1
movements[:,:40] = movements[:,:40]/imax[:40]
# Generate target vectors for all inputs 2 -> [0,1,0,0,0,0,0,0]
target = np.zeros((np.shape(movements)[0],8));
for x in range(1,9):
    indices = np.where(movements[:,40]==x)
    target[indices,x-1] = 1

# Randomly order the data
order = list(range(np.shape(movements)[0]))
np.random.shuffle(order)
movements = movements[order,:]
target = target[order,:]
# Split data into 3 sets

# Training updates the weights of the network and thus improves the network
train = movements[::2,0:40]
train_targets = target[::2]
# Validation checks how well the network is performing and when to stop
valid = movements[1::4,0:40]
valid_targets = target[1::4]

# Test data is used to evaluate how good the completely trained network is.
test = movements[3::4,0:40]
test_targets = target[3::4]

# Try networks with different number of hidden nodes:
hidden = 10

# Initialize the network:
net = mlp.mlp(train, train_targets, hidden)

# K-fold data management
'''
import random
random.seed(1)
def kfold(movements,target):
    k = 30
    percentage = float(k)/len(movements)
    print("percentage of set in validation: ",percentage)
    k_times = 10
    accuracy = np.zeros(k_times)
    for times in range(k_times):
        k_valid = random.sample(list(range(len(movements))),k)
        
        k_train = list(range(len(movements)))
        i = 0
        while len(k_train) > len(movements)-k:
            if k_train[i] in k_valid:
                k_train.pop(i)
            else:
                i+=1

        k_targets = []
        k_valid_targets = []

        for i in range(len(k_train)):
            s = k_train[i]
            k_train[i] = movements[s][0:40]
            k_targets.append(target[s])
        for i in range(len(k_valid)):
            s = k_valid[i]
            k_valid[i] = movements[s][0:40]
            k_valid_targets.append(target[s])
        net = mlp.mlp(np.asarray(k_train), np.asarray(k_targets), hidden)
        accuracy[times] = net.earlystopping(np.asarray(k_train), np.asarray(k_targets), np.asarray(k_valid), np.asarray(k_valid_targets))
    print("best model is model number: ", np.argmax(accuracy)," with validation accuracy = ", max(accuracy))
    print("mean of the accuracies = ", np.mean(accuracy))
    print("variance of the accuracies = ", np.sqrt(np.mean(accuracy**2)-np.mean(accuracy)**2))
kfold(movements,target)
'''
# Run training:

#net.train(train, train_targets, iterations=100) #wanna train without earlystopping?
net.earlystopping(train, train_targets, valid, valid_targets)


# Check how well the network performed:

net.confusion(test,test_targets)
net.confusion(valid,valid_targets)
