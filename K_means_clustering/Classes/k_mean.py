import random
from Classes.trajectory import *
from Classes.cluster import *

class k_mean:


    def __init__(self, max_distance=1, similarity_measure_type="LCESS"):
        self.max_distance = max_distance
        self.simmilarity_measure_type = similarity_measure_type

    def generate_random_means(self, k, trajectories):
        indexes = random.sample(range(len(trajectories)), int(k))
        random_means = []
        for index in indexes:
            random_means.append(trajectories[index])
        return random_means


    def k_means_iteration(self, trajectories, means, similarity_measure, dictionaries):
        moved_trajectoires = 0
        c = []
        for mean in means:
            c.append(cluster(mean, dictionaries, self.max_distance))
        for ci in c:
            ci.tr = []
        for index, t in enumerate(trajectories):
            distances = [similarity_measure.computeDistance(t, mean, self.simmilarity_measure_type) for mean in means]
            min_distance = min(distances)
            nearest_cluster_index = distances.index(min_distance)
            c[nearest_cluster_index].tr.append((t, min_distance))
            if t.cluster != nearest_cluster_index:
                moved_trajectoires += 1
                t.old_cluster = t.cluster
                t.cluster = nearest_cluster_index
        for index, ci in enumerate(c):
            ci.update_mean()
        return moved_trajectoires, c



    def k_means(self, k, input_trajectories, similarity_measure, dictionaries, iteration=100, min_change_percent_break=3, means=None):

        clusters = []
        changes=[]
        if means == None:

            means = self.generate_random_means(k, input_trajectories)

        random_means=means

        for i, r in enumerate(means):
            print("mean ", i)
            r.print()

        for i in range(iteration):
            moved_trajectories, clusters = self.k_means_iteration(input_trajectories, means, similarity_measure, dictionaries)
            means = []
            for cl in clusters:
                means.append(cl.mean)

            change_percent = moved_trajectories * 100 / len(input_trajectories)
            print("Iteration ", i + 1, " with ", int(change_percent), "% changes")
            print("----------------------------------------------------")
            for index, cl in enumerate(clusters):
                average_length, outOfOrder, avg_sim, number_of_trajectories, number_of_similar_trajectories, WSS = cl.cluster_info()
                print("cluster ", index + 1, " : average_length = ", int(average_length), ", outOfOrder(%) = ",
                      outOfOrder, " number of trajectories= ", len(cl.tr))

            changes.append(change_percent)
            if change_percent < min_change_percent_break or \
                    (len(changes) == 2 and changes[-1] == changes[-2]) or \
                    (len(changes) > 2 and changes[-1] == changes[-2] and changes[-1] == changes[-3]):
                break
        return clusters, random_means