import csv
import time
import numpy as np
from itertools import permutations
from functions import distance_matrix, partially_mapped, sort
np.random.seed(1)

with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

n_cities =10
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

    File = open("GA_result_of_%scities_and_%dpopulants.txt" % (n_cities,N_pop), "w")   
    File.write("These are the results for a poplation of size %d who %d times have jumped %d generations."%(N_pop,n_sims,generations))
    File.write("\n")
    File.write("For each generation, %d PMX operations create as many offspring as parents."%N_pop)
    File.write("\n")
    File.write("After each %d PMX operation, an elitist filter is applied to keep the population static and only the best solutions available. "%N_pop)
    File.write("\n")
    File.write("The sequences are printed to terminal since I'm having trouble writing them to file.")
    File.write("\n")
    best = [] #this boy picks the best of each simulation
    strd = 0  #this guy is for standard error measurements

    #Action
    for j in range(n_sims):
        for gen in range(generations):

            offspring = partially_mapped(parents,distances,n_cities,N_pop)

            new_population = np.append([offspring],[parents],axis=1)

            path_lengths, population = sort(new_population,distances)

            removables = len(path_lengths) - N_pop

            for i in range(removables) :
                path_lengths = np.delete(path_lengths,len(path_lengths)-1)
            parents = []
            for i in range(N_pop):
                parents.append(population[i])

        best.append(path_lengths[0]) #collecting shit for standard deviation
    
    best = np.asarray(best)
    print "%d cities, %d populants" % (n_cities,N_pop)
    print("best of the 20 individuals", min(best))
    print("worst of the 20 individuals", max(best))

    Mean = np.mean(best)
    Mean_sq = np.mean(best*best)
    standard_dev = np.sqrt(Mean_sq-Mean**2)
    print("standard dev of 20 best individuals", standard_dev)

    File.write("path lengths    sequences: ")
    File.write("\n")

    for i in range(N_pop):
        sequence = ''.join(str(number) for number in parents[i])
        File.write("  %.2f        %s" % (path_lengths[i], sequence))
        File.write("\n"% path_lengths[i])
    File.write(" ")
