import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

def prediction_testing(clusters, testing_trajectories, similarity_measure, similarity_measure_type="LCESS", prediction_threeshold = 70, maximum_distance_prediction_threeshold=0.6):
    '''

    :param clusters: results of the clustering ... Type: Array of cluster
    :param testing_trajectories: the trajectories to predict their physical state ... Type: Array of trajectory
    :param similarity_measure: reference to the similarity measure to use to calculate the similarity between the trajectories and the means ... Type: LCESSSim object
    :param similarity_measure_type: either LCESS or LCSS ... Type: String
    :param prediction_threeshold: The percentage of out-of-order docuements to consider a cluster out-of-order ... Type: Integer
    :param maximum_distance_prediction_threeshold: The maximum distance with the means, if the distance is more than the threeshold then the prediction is impossible ... Type: Integer
    :return: all_prediction: predictions on all the testing trajectories
            maximum_distance_prediction: predictions respecting the threeshold
            X_distances_to_the_means: Array from 0.1 to 1
            Y_distances_to_the_means: Array of integer ... Y_distances_to_the_means[0] The number the out-of-order documents classified as communicable having distance equal = X_distances_to_the_means[0]
    '''
    maximum_distance_prediction=[]
    all_prediction = []
    means = []
    X_distances_to_the_means = ["0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1"]
    Y_distances_to_the_means = [0]*11

    for cluster in clusters:
        means.append(cluster.mean)
    for trajectory in testing_trajectories:
        distances = [similarity_measure.computeDistance(trajectory, mean, similarity_measure_type) for mean in means]
        min_distance = min(distances)
        nearest_cluster_index = distances.index(min_distance)
        all_prediction.append((trajectory, clusters[nearest_cluster_index].percentOOO))

        if min_distance < maximum_distance_prediction_threeshold:
            maximum_distance_prediction.append((trajectory, clusters[nearest_cluster_index].percentOOO))

        if clusters[nearest_cluster_index].percentOOO < prediction_threeshold and trajectory.communicability == 0:
            rounded_sim = round(min_distance, 1)
            distance = 1-int(rounded_sim*10)
            Y_distances_to_the_means[distance] += 1

    return all_prediction, maximum_distance_prediction, X_distances_to_the_means, Y_distances_to_the_means


def results_characteristcs(allprediction, minimim_similaity_prediction):
    labels = [" Precision ", "Recall", "F-score"]
    x = np.arange(len(labels))
    width = 0.35  # the width of the bars

    Y_OOO = [0, 0]
    Y_communicable = [0, 0]

    for traj, pred_value in allprediction:
        if traj.communicability == 0:
            if pred_value < 70:
                Y_OOO[0] += 1
            else:
                Y_OOO[1] += 1
        else:
            if pred_value < 70:
                Y_communicable[0] += 1
            else:
                Y_communicable[1] += 1

    try:
        precision = round(Y_OOO[1]/(Y_communicable[1]+Y_OOO[1]), 2)
    except ZeroDivisionError:
        precision = 0
    try:
        recall = round(Y_OOO[1]/(Y_OOO[1]+Y_OOO[0]), 2)
    except ZeroDivisionError:
        recall = 0
    try:
        fScore = round((2*precision*recall)/(precision+recall), 2)
    except ZeroDivisionError:
        fScore = 0

    values = [precision, recall, fScore]

    Y_OOO = [0, 0]
    Y_communicable = [0, 0]

    for traj, pred_value in minimim_similaity_prediction:
        if traj.communicability == 0:
            if pred_value < 70:
                Y_OOO[0] += 1
            else:
                Y_OOO[1] += 1
        else:
            if pred_value < 70:
                Y_communicable[0] += 1
            else:
                Y_communicable[1] += 1
    fig, ax = plt.subplots()

    try:
        precision2 = round(Y_OOO[1] / (Y_communicable[1] + Y_OOO[1]), 2)
    except ZeroDivisionError:
        precision2 = 0
    try:
        recall2 = round(Y_OOO[1] / (Y_OOO[1] + Y_OOO[0]), 2)
    except ZeroDivisionError:
        recall2 = 0
    try:
        fScore2 = round((2 * precision2 * recall2) / (precision2 + recall2), 2)
    except ZeroDivisionError:
        fScore2 = 0
    values2 = [precision2, recall2, fScore2]

    rects1 = ax.bar(x - width / 2, values, width, label='All prediction')
    rects2 = ax.bar(x + width / 2, values2, width, label='Prediction with threeshold 0.4')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    listOf_Yticks = np.arange(0, 1, 3)
    plt.yticks(listOf_Yticks)
    plt.show()
    return recall2

def results_Plus_70(prediction, prediction_threshold = 70):

    labels = ["Classified as communicable ", "Classified as out-of-order"]
    x = np.arange(len(labels))
    width = 0.35  # the width of the bars
    Y_OOO = [0, 0]
    Y_communicable = [0, 0]

    for traj, pred_value in prediction:
        if traj.communicability == 0:
            if pred_value < prediction_threshold:
                Y_OOO[0] += 1
            else:
                Y_OOO[1] += 1
        else:
            if pred_value < 70:
                Y_communicable[0] += 1
            else:
                Y_communicable[1] += 1
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, Y_communicable, width, color=(0.3, 0.1, 0.4, 0.6), label='Communicable')
    rects2 = ax.bar(x + width / 2, Y_OOO, width, color=(0.3, 0.5, 0.4, 0.6), label='Out of order')
    ax.set_ylabel('Number of trajectories')
    ax.set_xlabel('Classification')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    plt.ion()
    plt.show()


def testing_results(prediction):

    labels = ["0%-25%", "25%-50%", "50%-75%", "75%-100%"]
    x = np.arange(len(labels))
    width = 0.35  # the width of the bars

    Y_OOO = [0, 0, 0, 0]
    Y_communicable = [0, 0, 0, 0]
    for traj, pred_value in prediction:
        if traj.communicability == 0:
            if pred_value < 25:
                Y_OOO[0] += 1
            elif pred_value < 50:
                Y_OOO[1] += 1
            elif pred_value < 75:
                Y_OOO[2] += 1
            else:
                Y_OOO[3] += 1
        else:
            if pred_value < 25:
                Y_communicable[0] += 1
            elif pred_value < 50:
                Y_communicable[1] += 1
            elif pred_value < 75:
                Y_communicable[2] += 1
            else:
                Y_communicable[3] += 1

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, Y_communicable, width, label='Communicable')
    rects2 = ax.bar(x + width / 2, Y_OOO, width, label='Out of order')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of documents')
    ax.set_xlabel('Classification')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()
