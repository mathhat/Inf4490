####Fix hill climber, it doesn't update best sequence. You should probably debug line by line
import csv
import time
import numpy as np

from itertools import permutations
with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

def distance_matrix(n_cities,data):
    distances = []       #list containing distances between cities
                         #This loop shortens the number of cities to the amount we want.
    for i in range(1,n_cities+1):
        distances.append(data[i][0:n_cities])
        for j in range(n_cities):             #This loop turns the distance str values into floating point values
            distances[i-1][j] = float(distances[i-1][j])
    return distances

#### Let's start from barcelona (reduces paths by a factor of n cities)

def barcelona(Permutations):
    i = 0
    while Permutations[i][0] == 0:    #This loop finds where the sequences beginning in Barcelona are.
        i += 1
                                    # Here we exlude the sequences who do not begin in Barcelona.
    return(Permutations[0:i])  #(cutting number of paths into one sixth of their original amount)
#Permutations = barcelona(Permutations)


#### This is a chaotic plot that helps us conclude to not optimize further.
'''
from matplotlib.pyplot import *

def mirrorplot(n_cities,Permutations):

    mirror = []
    for first_half in Permutations[0:(len(Permutations)/2)]:
        i = 0
        for sequence in Permutations:
            if list(reversed(sequence[1:n_cities])) == list(first_half[1:n_cities]):
                print(i)
                mirror.append(i)
                break
            else:
                i+=1
    plot(range(0,len(Permutations)/2),mirror)
    xlabel("Index of original Path")
    ylabel("Index of duplicate Path")
    show()
'''

                                                #return best sequence, distance traveled, time passed
def exhaustive(Permutations, distances,n_cities):

    Time = 0
    best = np.inf
    best_sequence = []
    start = time.time()             #start clock

    for sequence in Permutations:   #exhaustive search begins
        dist = 0
        for index in range(n_cities-1):
            dist += distances[sequence[index]][sequence[index+1]]
        dist += distances[sequence[n_cities-1]][sequence[0]]
        if dist < best:             #save shortest distance yet
            best=dist
            best_sequence = sequence

    end = time.time()              #end clock
    Time = (end-start)             #sum time
    return(best,best_sequence, Time)
#


def hillclimb(distances, n_cities,seed):             #Largely inspired by the book example
    np.random.seed(seed)  #updating seed gives different initial sequences per run

    sequence = np.asarray(range(n_cities))      #order of which cities we visit 

    np.random.shuffle(sequence)  #create a random initial order, from this -
                                 #order we make small hillclimbing changes
    
    distanceTravelled = np.inf   #this variable will be updated to the shortest path yet found

    i = 0                        #counter/loop variable to signify when we've made 1000 changes

    while i < 1000:
        newDistanceTravelled = 0 
        #declared numeric variable to compare a new -
        #path length to the previously shortest path.
        
        # Choose cities to swap
        city1 = np.random.randint(n_cities)     #2 random integers represents cities 
        city2 = np.random.randint(n_cities)     #-who's place in the initial path - 
                                                #are to be switched/reordered   
        if city1 != city2:                      
            i += 1              #If the cities are not the same, the operation is counted
                                #- because we wish to do this a limited amont of times (1000)
            # Reorder the set of cities
            possibleSequence = sequence.copy()
            possibleSequence = np.where(possibleSequence==city1,-1, possibleSequence)
            possibleSequence = np.where(possibleSequence==city2,city1, possibleSequence)
            possibleSequence = np.where(possibleSequence==-1,city2, possibleSequence)
            
            # Work out the new distances

            for j in range(n_cities-1): #Here I simply sum up the distance of the path like in exhaustive search
                newDistanceTravelled += distances[possibleSequence[j]][possibleSequence[j+1]]
            newDistanceTravelled += distances[possibleSequence[-1]][possibleSequence[0]]
            if newDistanceTravelled < distanceTravelled:
                distanceTravelled = newDistanceTravelled
                sequence = possibleSequence
    return sequence, distanceTravelled          #returns both path distance and which order the cities are traveled to