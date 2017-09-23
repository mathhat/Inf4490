import csv
import time
from itertools import permutations
import numpy as np
from functions import exhaustive, distance_matrix #the exhaustive function is the Exhaustive Search method.
                                                  #dist_matrix takes the 'data' matrix as its argument and
                                                  #- removes its first row, which consists of string names.
with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))



#File = open("time_exhaustive.txt","w")             #Writing runtimes to file, already done for n = 6:10 cities
Time_averages = []
Cities = range(10,11)

for n_cities in Cities:                          #varying number of city destinations
    Time = []                                        #gathers runtime
    distances = distance_matrix(n_cities,data)                    #grid and Permutations must be updated 
    Permutations = list(permutations(range(0,n_cities)))   #Here we create all possible permutations of n-city objects (paths)

                                      #for each time we increase city number


    for j in range(10):     #call function 10 times to get 10 time measurements
        best, best_seq, thyme = exhaustive(Permutations, distances, n_cities)  #returning runtime(thyme)

        Time.append(thyme)

        #File.write("Timestamp_%d for %d cities = %f seconds \n" %(j, n_cities, thyme))
    #File.write("\n")
    #File.write("Time average for %d cities = %f seconds \n" %(n_cities, sum(Time)/len(Time)) )
    #File.write("\n")
    Time_averages.append(sum(Time)/len(Time))       #Collect average runtime for plotting
    print("Shortest distance = ", best)
    print("Best sequence = ", best_seq)

#Plot of runtime as function of ncities
from matplotlib.pyplot import plot, show, xlabel, ylabel, title
plot(Cities,Time_averages)
xlabel("n cities")
ylabel("time [SEC]")
title("Time averages for the Exhaustive Search for n cities")
show()
