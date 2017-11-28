import csv
import time
import numpy as np
from itertools import permutations
from functions import distance_matrix, hillclimb

with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

n_cities = 24

n_sims = 20

lengths = np.zeros(n_sims)

distances = distance_matrix(n_cities,data)

for i in range(n_sims):
    seq, dist =  hillclimb(distances, n_cities,i)
    lengths[i]=dist
lengths=np.asarray(sorted(lengths))


Mean = np.mean(lengths)
Mean_sq = np.mean(lengths*lengths)
standard_dev = np.sqrt(Mean_sq-Mean**2)
print(standard_dev)




File = open("dist_hillclimber%scities.txt" % n_cities, "w")   

for i in range(len(lengths)):
    File.write("%.2f"%lengths[i])
    File.write("\n"%lengths[i])

File.write("\n"%lengths[i])
File.write("standard dev = %.2f"%standard_dev)


####I thought a histogram would look pretty but the results are too discontinuous
#import matplotlib.pyplot as mpl
#mpl.hist(lengths,bins=n_sims/2)
#mpl.show()