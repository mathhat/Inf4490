import csv
import time
from itertools import permutations
import numpy as np
from functions import exhaustive, grid #Exhaustive Search. Grid returns Permutations and Distance matrix
with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))



#File = open("time_exhaustive.txt","w")             #Writing runtimes to file, already done for n = 6:10 cities
Time_averages = []

for cities in range (6,11):                          #varying number of city destinations
    Time = []                                        #gathers runtime
    Permutations, distances = grid(cities,data)      #Permutations and grid must be updated 
                                                     #for each time we increase city number


    for j in range(10):     #call function 10 times to get 10 time measurements
        best, best_seq, thyme = exhaustive(Permutations, distances, cities)  #returning runtime(thyme)

        Time.append(thyme)

        #File.write("Timestamp_%d for %d cities = %f seconds \n" %(j, cities, thyme))
    #File.write("\n")
    #File.write("Time average for %d cities = %f seconds \n" %(cities, sum(Time)/len(Time)) )
    #File.write("\n")
    Time_averages.append(sum(Time)/len(Time))       #Collect average runtime for plotting

#Plot of runtime as function of ncities
from matplotlib.pyplot import plot, show, xlabel, ylabel, title
plot(range(6,11),Time_averages)
xlabel("n cities")
ylabel("time [SEC]")
title("Time averages for the Exhaustive Search for n cities")
show()