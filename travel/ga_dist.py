import csv
import time
import numpy as np
from itertools import permutations
from functions import distance_matrix, partially_mapped, sort
np.random.seed(0)

with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

n_cities =10
distances = distance_matrix(n_cities,data)

n_pop = [10,100,1000]
n_sims = 20

parents = np.zeros((n_pop[0],n_cities),int)  #creating parent array

for i in range(n_pop[0]):
    parents[i]= range(n_cities)

    np.random.shuffle(parents[i])


for j in range(10):

    offspring = partially_mapped(parents,distances,n_cities,n_pop[0])

    new_population = np.append([offspring],[parents],axis=1)

    path_lengths, population = sort(new_population,distances)

    removables = len(path_lengths) - n_pop[0]

    for i in range(removables) :
        path_lengths = np.delete(path_lengths,len(path_lengths)-1)
    parents = []
    for i in range(n_pop[0]):
        parents.append(population[i])



File = open("GA_result_of_%scities.txt" % n_cities, "w")   

File.write("path lengths in increasing order: ")
File.write("\n")

for i in range(n_pop[0]):
    File.write("%.2f" % path_lengths[i])
    File.write("\n"% path_lengths[i])
File.write(" ")
print ("sequence of cities in increasing path order: ")
for i in range(n_pop[0]):
    print(np.asarray(parents)[i])
File.write("")
File.write("These are the results for a poplation of size %d who 10 times have undergone %d PMX operations. "%(n_pop[0],n_pop[0]))
File.write("After each %d PMX operation, an elitist filter is applied to keep the population static and only the best solutions available"%n_cities)
File.write("The sequences printed to terminal since I'm having trouble writing them to file, I have to deliver in 15 minutes")