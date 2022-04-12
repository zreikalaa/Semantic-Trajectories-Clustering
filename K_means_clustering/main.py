import random
from Classes.dbQuerying import *
from Classes.LCESSSim import *
from Classes.ontologyQuerying import *
from Classes.trajectory import *
from Classes.cluster import *
from Classes.IG import *
import numpy as np


"""def calculate_distances(trajectories, dictionaries, ontology_depth):
    distance_matrix=[]
    lcss = LCSSSim(dictionaries, ontology_depth)
    print("calculate the similarities between ",len(trajectories)," trajectories")
    print("----------------------------------------------------------------")
    for i in range(len(trajectories)):
        distance_with_i=[]
        for j in range(len(trajectories)):
            if j%1000==0:
                print(j)
            if j==i:
                distance_with_i.append(0)
            elif j < i:
                distance_with_i.append(distance_matrix[j][i])
            else:
                distance_with_i.append(lcss.compute(trajectories[i],trajectories[j]))
        distance_matrix.append(distance_with_i)
        print("distances with the trajectory ",i," is calculated ",int(i*100/len(trajectories)))
    return distance_matrix
"""
if __name__ == '__main__':
    """
    k = 15
    connector = dbQuerying()
    trajectories = connector.getRandomTrajectories(dictionaries)
    print("clustering on ",len(trajectories)," trajectories")
    clusters = k_means(k, trajectories, lcss, dictionaries)
    """
    OQ = ontologyQuerying("crm_bnf.owl")
    ontology_depth, dictionaries = OQ.initialize_dictionaries()
    lcess = LCESSSim(dictionaries, ontology_depth)
    ig = IG(lcess, dictionaries)


