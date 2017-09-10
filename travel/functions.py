import csv
import time
import numpy as np
from itertools import permutations
with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

def grid(cities,data):
    distances = []       #list containing distances between cities
                                                #This loop shortens the number of cities to the amount we want.
        for i in range(1,cities+1):
            distances.append(data[i][0:cities])
            for j in range(cities):             #This loop turns the distance str values into floating point values
                distances[i-1][j] = float(distances[i-1][j])

        Permutations = list(permutations(range(0,cities)))      #Here we create all possible permutations of n-city objects (paths)
    return(Permutations, distances)


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
def mirrorplot():

    mirror = []
    for first_half in Permutations[0:(len(Permutations)/2)]:
        i = 0
        for sequence in Permutations:
            if list(reversed(sequence[1:cities])) == list(first_half[1:cities]):
                print(i)
                mirror.append(i)
                break
            else:
                i+=1
    from matplotlib.pyplot import *
    plot(range(0,len(Permutations)/2),mirror)
    xlabel("Index of original Path")
    ylabel("Index of duplicate Path")
    show()


'''

                                                #return best sequence, distance traveled, time passed
def exhaustive(Permutations, distances,cities):
    Time = 0
    best = np.inf
    best_sequence = []
    start = time.time()             #start clock

    for sequence in Permutations:   #exhaustive search begins
        dist = 0
        for index in range(cities-1):
            dist += distances[sequence[index]][sequence[index+1]]
        dist += distances[sequence[cities-1]][sequence[0]]
        if dist < best:             #save shortest distance yet
            best=dist
            best_sequence = sequence

    end = time.time()              #end clock
    Time = (end-start)             #sum time
    return(best,best_sequence, Time)


