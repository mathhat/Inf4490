import csv
import time
import numpy as np
from itertools import permutations
from functions import distance_matrix, hillclimb

with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

n_cities = 10

n_sims = 200

swag = np.zeros(n_sims)

distances = distance_matrix(n_cities,data)

for i in range(n_sims):
    seq, dist =  hillclimb(distances, n_cities)
    print("sequence: ",seq,"  distancetraveled = ",dist," run # ",i)
    swag[i]=dist
import matplotlib.pyplot as mpl
mpl.hist(swag,bins=n_sims/2)
mpl.show()