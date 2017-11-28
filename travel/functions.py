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


def partially_mapped(parents, distances, n_cities, n_pop):
    
    offspring = np.zeros((n_pop,n_cities),int)    #matrix n_population x n_cities

    for iterations in range(n_pop):
        #Choosing parents to mate
        parent12 = np.random.randint(0,n_pop,2,int)
        parent1 = min(parent12)
        parent2 = max(parent12)
        index1 = np.random.randint(0,n_cities)
        index2 = index1+2
        if (index1 != index2) and (parent1 != parent2) :  #Making sure parents are different and -
            #Here starts the partially mapped crosseover

            #initial kids are identical to parents

            offspring[iterations] = parents[parent1]


            #crossover genomes/sequences
            genome1 = parents[parent1][index1:index2]
            genome2 = parents[parent2][index1:index2]

            #inserting genomes
            offspring[iterations][index1:index2] = genome2 #offspring 1 gets sequence from parent 2
            #crossover from parents to offspring 1
            for i in range(len(genome2)):
                if genome1[i] in genome2:
                    pass
                else:
                    gene = genome2[i]
                    success = 0
                    while success == False:
                        if gene == genome2[np.where(genome1==gene)]:
                            success = True
                            pass
                        if gene in genome1:
                            gene = genome2[np.where(genome1==gene)]
                        else:
                            offspring[iterations][np.where(parents[parent1]==gene)] = genome1[i]
                            success = True
    return offspring

def sort(pop_matrix,distances): 
    population = []     #best solutions
    path_lengths = []   #way of finding best solutions
    pop_matrix = pop_matrix[0] 

    n_cities = len(pop_matrix[0]) #city number
    for sequence in pop_matrix:   #first calculate path lenths
        dist = 0
        if sum(sequence)>0:       #ignores sequences like [0,0,0,0,0]
            for index in range(n_cities-1):
                dist += distances[sequence[index]][sequence[index+1]]
            dist += distances[sequence[n_cities-1]][sequence[0]]
            population.append(sequence)
            path_lengths.append(dist)

    population = np.asarray(population)
    path_lengths = np.asarray(path_lengths)

    ranked_paths = []
    ranked_sequences = []
    for i in range(len(population)): #then arrange them in diminishing order
        ranked_paths.append(np.amin(path_lengths))
        ranked_sequences.append(population[np.argmin(path_lengths)])
        path_lengths = np.delete(path_lengths, np.argmin(path_lengths)) 
        
    return np.asarray(ranked_paths), np.asarray(ranked_sequences)




def hillclimb2(sequence,distances):             #same as above, but called differently
    distanceTravelled = np.inf   #this variable will be updated to the shortest path yet found

    i = 0                        #counter/loop variable to signify when we've made 1000 changes
    n_cities = len(sequence)
    while i < 2:
        
        newDistanceTravelled = 0 
        #declared numeric variable to compare a new -
        #path length to the previously shortest path.
        
        # Choose cities to swap
        city1 = np.random.randint(n_cities)     #2 random integers represents cities 
        city2 = np.random.randint(n_cities)     #-who's place in the initial path - 
                                                #are to be switched/reordered   
        if city1 != city2:                      
            i += 1                        #- because we wish to do this a limited amont of times (1000)
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
                              #If the cities are not the same, the operation is counted

    return sequence, distanceTravelled          #returns both path distance and which order the cities are traveled to
