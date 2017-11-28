'''
    This pre-code is a nice starting point, but you can
    change it to fit your needs.
'''
import numpy as np
np.random.seed(1)
class mlp:
    def __init__(self, inputs, targets, nhidden):
        self.inputs2 = np.zeros((len(inputs),len(inputs[0])+1))
        for i in range(len(inputs)):
            for j in range(len(inputs[0])):
                self.inputs2[i,j] = inputs[i,j]
            self.inputs2[i,40] = -1
        self.beta = 1
        self.eta = 0.1
        self.momentum = 0.0
        
        #Weights are given an extra index for the bias input
        self.weights1 = np.random.random((nhidden,len(inputs[0]) + 1))*1./np.sqrt(nhidden+1) #scaling constant
        #weights between input n hidden
        self.weights2 = np.random.random((len(targets[0]),nhidden+1))*1./np.sqrt(len(targets[0])+1)
        #weights between hidden and output

        #the following forloops randomly mirror the weights around 0 (so we get negative weights too)

        for j in range(nhidden):
            for i in range(len(inputs[0])-1):
                if (np.random.randint(2)): 
                    self.weights1[j,i] = self.weights1[j,i]*(-1)   
        for i in range(nhidden-1):
            for j in range(len(targets[0])):
                if (np.random.randint(2)): 
                    self.weights2[j,i] = self.weights2[j,i]*(-1)

        self.y_h = np.zeros((len(inputs),nhidden+1))
        self.y_h[:][-1] -= 1

        self.y = np.zeros((len(inputs),len(targets[0])))

        self.error_sqrd_sum = 0


    # You should add your own methods as well!

    def g(self, h):                    #spike function
        return(1./(1+np.exp(-self.beta*h)))

    def add_up(self, w, x):             #vector dot product
        return (sum(w * x))
    
    def earlystopping(self, inputs, targets, valid, validtargets):
        maxiter = 5000
        checkpoint = 15 #each time we check if accuracy in validation set is failing
        self.train(inputs,targets,checkpoint) #initial training
        accuracy0 = self.confusion(valid,validtargets)  #initial accuracy
        local_optima_dodger = 0
        
        for i in range(2,int(maxiter/checkpoint)):
            self.train(inputs,targets,checkpoint)#checkpoint*i)
            accuracy = self.confusion(valid,validtargets)
            if accuracy <= accuracy0:
                local_optima_dodger +=1
            else:
                accuracy0 = accuracy
            if local_optima_dodger > 15:
                break   

        print("final validation accuracy = ", accuracy0)
        print("number of iterations of max 5000: ", ((1+i)*checkpoint ))
        return(accuracy)

    def train(self, inputs, targets, iterations):
        for I in range(iterations):
            self.forward(inputs)
            w2 = self.weights2
            w1 = self.weights1

            y = self.y
            y_h = self.y_h

            delta_k = (y-targets)*y*(1-y)
            delta_h = y_h*(1-y_h)*np.dot(delta_k,w2)

            w1 -= self.eta* np.dot(delta_h[:,:-1].T,self.inputs2)
            w2 -= self.eta*np.dot(delta_k.T, y_h)

    def recall(self, inputs):
        n=0
        v = self.weights1
        w = self.weights2
        #copy paste of most of the forward function
        for i in range(len(self.y_h[n])-1):
            self.y_h[n,i] = self.g(self.add_up(np.append(inputs, [-1]),v[i,:]))
        for i in range(len(self.y[n])):
            self.y[n,i] = self.g(self.add_up(self.y_h[n], w[i,:]))

        swag = np.copy(self.y[n])
        swag[np.argmax(swag)] = 1
        return(np.round(swag))


    def forward(self, inputs):
        v = self.weights1
        w = self.weights2
        for n in range(len(inputs)):
            for i in range(len(self.y_h[n])-1):
                self.y_h[n,i] = self.g(self.add_up(np.append(inputs[n], [-1]),v[i,:]))
            for i in range(len(self.y[n])):
                self.y[n,i] = self.g(self.add_up(self.y_h[n], w[i,:]))
        

    def confusion(self, inputs, targets):
        self.conf = np.zeros((len(targets[0]),len(targets[0])))
        non_spikes = 0
        for i in range(len(inputs)):
            recall = self.recall(inputs[i])
            if 1 in recall:
                self.conf[np.argmax(targets[i]),np.argmax(recall)] += 1
            else:
                non_spikes +=1
        accuracy = float(np.trace(self.conf))/(np.sum(self.conf)+non_spikes)
        print(self.conf)
        print(accuracy)
        return(accuracy)
