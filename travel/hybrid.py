import csv
import time
import numpy as np
from itertools import permutations
from matplotlib.pyplot import *
from functions import distance_matrix, partially_mapped, sort, hillclimb2
np.random.seed(5)

with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

n_cities =24
distances = distance_matrix(n_cities,data)

n_pop = [10,100,1000]
n_sims = 20      # runs
generations = 10 # generations per run


#for p in n_pop:

for N_pop in n_pop:
    parents = np.zeros((N_pop,n_cities),int)  #creating parent array

    for i in range(N_pop):
        parents[i]= range(n_cities)

        np.random.shuffle(parents[i])
    best = [] #this boy picks the best of each simulation
    strd = 0  #this guy is for standard error measurements
    means = []

    #Action
    for j in range(n_sims):
        for gen in range(generations):

            offspring = partially_mapped(parents,distances,n_cities,N_pop)

            new_population = np.append([offspring],[parents],axis=1)

            path_lengths, population = sort(new_population,distances)

            removables = len(path_lengths) - N_pop

            for i in range(removables):
                path_lengths = np.delete(path_lengths,len(path_lengths)-1)
            parents = []
            for i in range(N_pop):
                parents.append(population[i])
    
        for populant in range(N_pop): 
            parents[populant], path_lengths[populant] =  hillclimb2(parents[populant],distances)

            
        means.append(np.mean(path_lengths))
        best.append(path_lengths[0]) #collecting shit for standard deviation
    '''plot(range(n_sims),means)
    title("Average fitness for 24 Cities problem")
    xlabel("Run")
    ylabel("Average fitness")
    show()
    '''
    best = np.asarray(best)
    print "%d cities, %d populants" % (n_cities,N_pop)
    print("best of the 20 individuals", min(best))
    print("worst of the 20 individuals", max(best))

    Mean = np.mean(best)
    Mean_sq = np.mean(best*best)
    standard_dev = np.sqrt(Mean_sq-Mean**2)
    print("standard dev of 20 best individuals", standard_dev)