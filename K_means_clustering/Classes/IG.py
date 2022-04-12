import tkinter as tk
from tkinter import *
from Classes.cluster import *
from Classes.dbQuerying import *
import math
from collections import Counter
from images import *
from PIL import ImageTk, Image
import time
from Classes.k_mean import *
from Classes.testing import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class IG:

    def __init__(self, similarity_measure, dictionaries):
        self.clusters = []
        self.clusters2 = []
        self.random_means = ""
        self.dictionaries = dictionaries
        self.similarity_measure = similarity_measure

        self.CANVAS_WIDTH, self.CANVAS_HEIGHT = 600, 800
        root = tk.Tk()
        self.root = root

        self.data_loaded = 0

        self.entries_ref=[]
        #---------Load data frame-----------------

        load_data_frame = tk.LabelFrame(root, text="Load Data")
        numberOOO_lbl = tk.Label(load_data_frame, text="Number of Out-of-Order documents")
        numberOOO_lbl.grid(column=0, row=0)
        numberOOO_entry = tk.Entry(load_data_frame)
        numberOOO_entry.grid(column=1, row=0)
        self.entries_ref.append(numberOOO_entry)

        percentOOO_lbl = tk.Label(load_data_frame, text="Percentage of Out-of-Order documents")
        percentOOO_lbl.grid(column=0, row=1)
        percentOOO_entry = tk.Entry(load_data_frame)
        percentOOO_entry.grid(column=1, row=1)
        self.entries_ref.append(percentOOO_entry)

        percent_test_lbl = tk.Label(load_data_frame, text="Percentage of testing set")
        percent_test_lbl.grid(column=0, row=2)
        percent_test_entry = tk.Entry(load_data_frame)
        percent_test_entry.grid(column=1, row=2)
        self.entries_ref.append(percent_test_entry)

        miminum_length_lbl = tk.Label(load_data_frame, text="Minimum trajectory length")
        miminum_length_lbl.grid(column=0, row=3)
        miminum_length_scale = tk.Scale(load_data_frame, from_=1, to=25, activebackground="blue", orient=tk.HORIZONTAL)
        miminum_length_scale.set(3)
        miminum_length_scale.grid(column=1, row=3)

        maximum_length_lbl = tk.Label(load_data_frame, text="Maximum trajectory length")
        maximum_length_scale = tk.Scale(load_data_frame, from_=1, to=25, activebackground="blue", orient=tk.HORIZONTAL)
        maximum_length_scale.set(10)
        maximum_length_lbl.grid(column=0, row=4)
        maximum_length_scale.grid(column=1, row=4)

        load_data_button = tk.Button(load_data_frame, text="Load data", command=lambda:
                                                        self.load_data(
                                                        percent_OOO_entry = percentOOO_entry,
                                                        minimum_length_scale = miminum_length_scale,
                                                        maximum_length_scale = maximum_length_scale,
                                                        number_OOO_entry = numberOOO_entry,
                                                        percent_test_entry = percent_test_entry
                                                        ))
        load_data_button.grid(column=0, row=6)
        load_data_msg_lbl = tk.Label(load_data_frame)
        self.load_data_msg_lbl = load_data_msg_lbl
        load_data_msg_lbl.grid(column=1, row=6)
        # ----------------------------------------------

        # ---------Clustering frame---------------------
        clustering_frame = tk.LabelFrame(root, text="Clustering")

        k_lbl = tk.Label(clustering_frame, text="Starting K")
        k_lbl.grid(column=0, row=0)
        k_entry = tk.Entry(clustering_frame)
        k_entry.grid(column=1, row=0)
        self.entries_ref.append(k_entry)

        mean_minimum_similarity_lbl = tk.Label(clustering_frame, text="Maximum distance with the means")
        mean_minimum_similarity_lbl.grid(column=0, row=1)
        mean_minimum_similarity_scale= tk.Scale(clustering_frame, from_=0, to=1, activebackground="blue", resolution=0.05, orient=tk.HORIZONTAL)
        mean_minimum_similarity_scale.set(0.2)
        mean_minimum_similarity_scale.grid(column=1, row=1)

        clustering_button = tk.Button(clustering_frame, text="Start", command=lambda:
                                                            self.clustering(
                                                            k_entry=k_entry,
                                                            mean_maximum_distance_scale=mean_minimum_similarity_scale
                                                            ))
        clustering_button.grid(column=0, row=3)

        continue_clustering_button = tk.Button(clustering_frame, text="Remove outliers and continue!", fg="red", state=tk.DISABLED, command=lambda:
        self.removing_outliers_and_clustering(
            k_entry=k_entry,
            mean_minimum_distance_scale=mean_minimum_similarity_scale
        ))
        self.continue_clustering_button=continue_clustering_button
        continue_clustering_button.grid(column=1, row=3)

        self.var = tk.IntVar()
        R1 = tk.Radiobutton(clustering_frame, text="Windows 1", variable=self.var, value=1)
        R1.grid(column=0, row=4)

        R2 = tk.Radiobutton(clustering_frame, text="Windows 2", variable=self.var, value=2)
        R2.grid(column=1, row=4)

        self.similarity_measure_type = tk.IntVar()
        R1 = tk.Radiobutton(clustering_frame, text="LCESS", variable=self.similarity_measure_type, value=1)
        R1.grid(column=0, row=5)

        R2 = tk.Radiobutton(clustering_frame, text="LCSS", variable=self.similarity_measure_type, value=2)
        R2.grid(column=1, row=5)



        # ----------------------------------------------

        # ------------ K affection frame----------------

        k_affection_frame = tk.LabelFrame(root, text="K affection", fg="red")

        from_lbl = tk.Label(k_affection_frame, text="From")
        from_lbl.grid(column=0, row=0)
        from_scale = tk.Scale(k_affection_frame, from_=1, to=100, activebackground="blue", orient=tk.HORIZONTAL)
        from_scale.set(3)
        from_scale.grid(column=1, row=0)

        to_lbl = tk.Label(k_affection_frame, text="To")
        to_lbl.grid(column=0, row=1)
        to_scale = tk.Scale(k_affection_frame, from_=1, to=100, activebackground="blue", orient=tk.HORIZONTAL)
        to_scale.set(10)
        to_scale.grid(column=1, row=1)

        k_button = tk.Button(k_affection_frame, text="Calculate", command=lambda:
        self.k_affection(
            from_scale=from_scale,
            to_scale=to_scale
                         ))
        k_button.grid(column=0, row=2)
        # ----------------------------------------------

        # ------------------- Testing ------------------
        testing_frame = tk.LabelFrame(root, text="Testing")

        testing1_button = tk.Button(testing_frame, text="Test on Clusters 1", state=tk.DISABLED, command=lambda:
        prediction_testing(
            clusters=self.clusters,
            testing_trajectories=self.testing_trajectories,
            similarity_measure=self.similarity_measure
        ))
        self.testing1_button = testing1_button
        testing1_button.grid(column=0, row=0)

        normal_testing_button = tk.Button(testing_frame, text="Normal test", command=lambda:
        self.normal_test_results())
        normal_testing_button.grid(column=0, row=1)

        similarities_test_button = tk.Button(testing_frame, text="Similarities test", command=lambda:
        self.similarities_test_results())
        similarities_test_button.grid(column=0, row=2)

        test_with_threeshold_button = tk.Button(testing_frame, text="Test with threeshold", command=lambda:
        self.test_with_threeshold_results())
        test_with_threeshold_button.grid(column=0, row=3)

        results_button = tk.Button(testing_frame, text="F-score", command=lambda:
        results_characteristcs(self.all_prediciton, self.minimuum_similarity_prediction))
        results_button.grid(column=0, row=4)

        lcss_vs_lcess_button = tk.Button(testing_frame, text="LCSS VS LCESS Prediction", command=lambda:
        self.lcssVslcessVis())
        lcss_vs_lcess_button.grid(column=0, row=5)

        testing2_button = tk.Button(testing_frame, text="Test on Clusters 2", state=tk.DISABLED, command=lambda:
        prediction_testing(
            clusters=self.clusters2,
            testing_trajectories=self.testing_trajectories,
            similarity_measure=self.similarity_measure
        ))
        self.testing2_button = testing2_button
        testing2_button.grid(column=1, row=0)
        # ----------------------------------------------

        # --------- Testing the parameters frame -------

        """testing_parameters_frame = tk.LabelFrame(root, text="Testing the parameters", fg="red")

        threeshold_button = tk.Button(testing_parameters_frame, text="Threeshold affection", command=lambda:
        self.threeshold_affection())
        threeshold_button.grid(column=0, row=0)

        outliers_button = tk.Button(testing_parameters_frame, text="Outliers affection", command=lambda:
        self.outliers_affection())
        outliers_button.grid(column=0, row=1)"""

        # ----------------------------------------------

        # ---------Weighting ontology frame-------------
        weighting_frame = tk.LabelFrame(root, text="Weighting the ontology with linear regression (TO DO)", fg="red")
        ontology_lbl = tk.Label(weighting_frame, text="Ontology")
        ontology_lbl.grid(column=0, row=0)
        ontology_entry = tk.Entry(weighting_frame, text="CRM_BnF")
        ontology_entry.insert(0, "CRM_BnF.owl")
        ontology_entry.grid(column=1, row=0)

        weighting_button = tk.Button(weighting_frame, text="Weighting the ontology using the loaded data!", fg="red", command=lambda:
        self.weighting())

        weighting_button.grid(column=0, row=2, columnspan=2)
        # ----------------------------------------------

        load_data_frame.grid(row=0, column=0)
        clustering_frame.grid(row=1, column=0)
        testing_frame.grid(row=2, column=0)
        k_affection_frame.grid(row=3, column=1)
        weighting_frame.grid(row=3,column=2)
        reset_button = tk.Button(root, text="Reset", fg="red",
                                     command=lambda:
                                     self.reset())
        reset_button.grid(row=3, column=3)
        canvas = tk.Canvas(root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg="white",relief="raised",bd=5)
        canvas.grid(column=1, row=0, rowspan=3)
        canvas.bind("<Button-1>", lambda event, canvas_id=1:
                            self.clicked(event, canvas_id))
        self.canvas = canvas
        canvas2 = tk.Canvas(root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg="white", relief="raised", bd=5)
        canvas2.grid(column=2, row=0, rowspan=3)
        canvas2.bind("<Button-1>", lambda event, canvas_id=2:
                            self.clicked(event, canvas_id))
        self.canvas2 = canvas2
        root.geometry("1000x1000")
        root.mainloop()


    def similarity_measure_Testing(self, clusters, similarity_measure_type="LCESS", threeshold=0.6):

        self.all_prediciton, self.minimuum_similarity_prediction, self.X_distances_to_the_means, self.Y_distances_to_the_means = \
            prediction_testing(clusters, testing_trajectories=self.testing_trajectories,
                               similarity_measure=self.similarity_measure, similarity_measure_type=similarity_measure_type, maximum_distance_prediction_threeshold=threeshold)
        results_Plus_70(self.all_prediciton)
        self.similarities_test_results()
        results_Plus_70(self.minimuum_similarity_prediction)
        precision = results_characteristcs(self.all_prediciton, self.minimuum_similarity_prediction)
        prediction_percentage = len(self.minimuum_similarity_prediction) * 100 / len(self.all_prediciton)

        return precision, prediction_percentage

    def lcssVsLcess(self, threeshold=0.6):
        k = 8
        mean_maximum_distance = threeshold

        km = k_mean(mean_maximum_distance, "LCESS")
        clusters_lcess, random_means = km.k_means(k, self.training_trajectories, self.similarity_measure, self.dictionaries)

        km.simmilarity_measure_type="LCSS"
        clusters_lcss, random_means = km.k_means(k, self.training_trajectories, self.similarity_measure, self.dictionaries,
                                            means=random_means)

       #------------------LCESS testing------------------

        LCESS_precision, LCESS_prediction_percentage=self.similarity_measure_Testing(clusters_lcess, "LCESS")

        # ------------------LCSS testing------------------

        LCSS_precision, LCSS_prediction_percentage = self.similarity_measure_Testing(clusters_lcss, "LCSS")

        return LCSS_precision, LCSS_prediction_percentage, LCESS_precision, LCESS_prediction_percentage

    def lcssVslcessVis(self):

        k = 8
        threesholds=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] #Maximum distance with the mean, if the distance is more than the threeshold the prediction is impossible
        LCSS_precisions=[]
        LCSS_prediction_percentages = []
        LCESS_precisions = []
        LCESS_prediction_percentages = []

        km = k_mean(0.5, "LCESS")
        clusters_lcess, random_means = km.k_means(k, self.training_trajectories, self.similarity_measure,
                                                  self.dictionaries)

        km.simmilarity_measure_type = "LCSS"
        clusters_lcss, random_means = km.k_means(k, self.training_trajectories, self.similarity_measure,
                                                 self.dictionaries,
                                                 means=random_means)


        for threeshold in threesholds:

            LCESS_precision, LCESS_prediction_percentage = self.similarity_measure_Testing(clusters_lcess, "LCESS", threeshold=threeshold)
            LCSS_precision, LCSS_prediction_percentage = self.similarity_measure_Testing(clusters_lcss, "LCSS", threeshold=threeshold)

            LCSS_precisions.append(LCSS_precision)
            LCSS_prediction_percentages.append(LCSS_prediction_percentage)
            LCESS_precisions.append(LCESS_precision)
            LCESS_prediction_percentages.append(LCESS_prediction_percentage)


        width = .35  # width of a bar

        m1_t = pd.DataFrame({
            'PrecisionLcess': LCESS_precisions,
            'DocumentsPercentageLcess': LCESS_prediction_percentages,
            })

        m1_t[['PrecisionLcess']].plot(kind='bar', width=width)
        m1_t['DocumentsPercentageLcess'].plot(secondary_y=True, color="red")

        ax = plt.gca()
        plt.xlim([-width, len(m1_t['PrecisionLcess']) - width])
        ax.set_xticklabels(('0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'))

        plt.show()

        m1_t = pd.DataFrame({
            'Precision': LCSS_precisions,
            'DocumentsPercentage': LCSS_prediction_percentages})

        m1_t[['Precision']].plot(kind='bar', width=width)
        m1_t['DocumentsPercentage'].plot(secondary_y=True, color="green")

        ax = plt.gca()
        plt.xlim([-width, len(m1_t['Precision']) - width])
        ax.set_xticklabels(('0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'))

        plt.show()

    def normal_test_results(self):
        results_Plus_70(self.all_prediciton)

    def similarities_test_results(self):
        x = np.arange(len(self.X_distances_to_the_means))
        fig, ax = plt.subplots()
        ax.plot(self.X_distances_to_the_means, self.Y_distances_to_the_means)
        print(self.Y_distances_to_the_means)
        ax.set_ylabel('Number of documents')
        ax.set_xlabel('Distance')
        ax.set_xticks(x)
        ax.set_xticklabels(self.X_distances_to_the_means)
        fig.tight_layout()
        plt.show()

    def test_with_threeshold_results(self):
        results_Plus_70(self.minimuum_similarity_prediction)

    def reset(self):
        for entry in self.entries_ref:
            entry.delete(0, 'end')

        self.canvas.delete("all")
        self.canvas2.delete("all")

        self.clusters2 = []
        self.clusters = []
        self.continue_clustering_button['state'] = tk.DISABLED
        self.data_loaded = 0
        self.var = tk.IntVar()

    def k_affection(self, from_scale, to_scale):
        from_value = int(from_scale.get())
        to_value = int(to_scale.get())
        X = []
        Y = []
        km = k_mean()
        for k in range(from_value, to_value):
            clusters = km.k_means(k, self.training_trajectories, self.similarity_measure, self.dictionaries)
            X.append(k)
            TWSS = self.clustering_homogeneity(clusters)
            Y.append(TWSS)
            print(" WSS= ",TWSS," with k = ",k)

        for i in range(1,len(Y)):
            if Y[i]>Y[i-1]:
                    Y[i] = Y[i - 1]


        plt.plot(X,Y)
        plt.ylabel('WSS')
        plt.xlabel("k")
        plt.show()

    def  clustering_homogeneity(self, clusters):
        homogeneity = 0
        total_number_of_trajectories = 0
        TWSS=0
        for cluster in clusters:
            avg_length, outOfOrder, avg_sim, number_of_trajectories, number_of_similar_trajectories, WSS = cluster.cluster_info()
            homogeneity += number_of_trajectories*avg_sim
            total_number_of_trajectories += number_of_trajectories
            TWSS+=WSS

        return TWSS

    def load_data(self, minimum_length_scale, maximum_length_scale, percent_OOO_entry, number_OOO_entry, percent_test_entry):
        connector = dbQuerying()
        out_of_order_percent = int(percent_OOO_entry.get())
        minimum_length = int(minimum_length_scale.get())
        maximum_length = int(maximum_length_scale.get())
        out_of_order = int(number_OOO_entry.get())
        percent_test = int(percent_test_entry.get())

        trajectories_ooo, trajectories_communicable = connector.getRandomTrajectories(self.dictionaries,
                                                            out_of_order_percent = out_of_order_percent,
                                                            miminum_length = minimum_length,
                                                            maximum_length = maximum_length,
                                                            out_of_order = out_of_order)
        random.shuffle(trajectories_communicable)
        random.shuffle(trajectories_ooo)

        number_of_ooo=len(trajectories_ooo)
        number_of_communicable=len(trajectories_communicable)

        number_of_ooo_training = int(number_of_ooo*(100-percent_test)/100)
        number_of_communicable_training = int(number_of_communicable*(100-percent_test)/100)


        self.training_trajectories = []
        self.testing_trajectories = []

        self.training_trajectories.extend(trajectories_ooo[0:number_of_ooo_training])
        self.training_trajectories.extend(trajectories_communicable[0:number_of_communicable_training])

        self.testing_trajectories.extend(trajectories_ooo[number_of_ooo_training:])
        self.testing_trajectories.extend(trajectories_communicable[number_of_communicable_training:])

        print("training= ", len(self.training_trajectories))
        print("testing= ", len(self.testing_trajectories))

        self.load_data_msg_lbl.config(text="Data Loaded Successfully",fg='green')
        self.data_loaded = 1
        #self.lcssVslcessVis()


    def clustering(self, k_entry, mean_maximum_distance_scale):
        canvas = None
        if str(self.var.get()) == str(1):
            canvas=self.canvas
        elif str(self.var.get()) == str(2):
            canvas = self.canvas2
        if canvas != None:
            canvas.delete("all")

        k = k_entry.get()
        mean_maximum_distance = mean_maximum_distance_scale.get()
        if str(self.similarity_measure_type.get()) == str(1):
            similarity_measure_type="LCESS"
        else:
            similarity_measure_type="LCSS"


        km=k_mean(mean_maximum_distance, similarity_measure_type)
        self.km = km

        if self.random_means != "":
            clusters, random_means = km.k_means(k, self.training_trajectories, self.similarity_measure, self.dictionaries, means=self.random_means)
        else:
            clusters, random_means = km.k_means(k, self.training_trajectories, self.similarity_measure, self.dictionaries)

        self.random_means = random_means

        if str(self.var.get()) == str(1):
            self.clusters = clusters
            self.testing1_button['state'] = tk.NORMAL
        elif str(self.var.get()) == str(2):
            self.clusters2 = clusters
            self.testing2_button['state'] = tk.NORMAL

        self.draw_clusters(clusters)
        self.clustering_checking(clusters)
        self.continue_clustering_button['state'] = tk.NORMAL


    def removing_outliers_and_clustering(self, k_entry, mean_minimum_distance_scale):
        k = k_entry.get()
        mean_minimum_sim = mean_minimum_distance_scale.get()

        clusters=[]
        if str(self.var.get()) == str(1):
            clusters = self.clusters2
        elif str(self.var.get()) == str(2):
            clusters = self.clusters

        means=[]
        trajectories = []

        for cluster in clusters:
            tr = cluster.removing_outliers()
            means.append(cluster.mean)
            trajectories.extend([i[0] for i in tr])

        km = k_mean(mean_minimum_sim)
        clusters = km.k_means(k, trajectories, self.similarity_measure, self.dictionaries, means=means)

        if str(self.var.get()) == str(1):
            self.clusters = clusters
            self.testing1_button['state'] = tk.NORMAL
        elif str(self.var.get()) == str(2):
            self.clusters2 = clusters
            self.testing2_button['state'] = tk.NORMAL

        self.draw_clusters(clusters, removing_outliers=1)
        self.clustering_checking(clusters)


    def clustering_checking(self, clusters):
        means=[]
        errors=0
        if str(self.similarity_measure_type.get()) == str(1):
            similarity_measure_type="LCESS"
        else:
            similarity_measure_type="LCSS"
        for cluster in clusters:
            means.append(cluster.mean)

        for traj in self.training_trajectories:

            distances = [self.similarity_measure.computeDistance(traj, mean, similarity_measure_type) for mean in means]
            min_distance = min(distances)
            nearest_cluster_index = distances.index(min_distance)
            if nearest_cluster_index != traj.cluster:
                errors += 1

        print(errors," unstable trajectories")


    def clicked(self, event, canvas_id):
        if canvas_id==1:
            cnv = self.canvas
            clusters = self.clusters
        else:
            cnv = self.canvas2
            clusters = self.clusters2

        item = cnv.find_closest(cnv.canvasx(event.x), cnv.canvasy(event.y))[0]
        tags = cnv.gettags(item)
        cluster_index=tags[0]

        newWindow = tk.Toplevel(self.root)
        newWindow.title("cluster "+cluster_index)
        newWindow.geometry("800x400")

        cluster = clusters[int(cluster_index)]

        mean_length=len(cluster.mean.events)
        meanLbl = tk.Label(newWindow, text=cluster.mean.print()
                         , font=("helvetica", "10"))
        meanLbl.grid(column=0,row=0,columnspan=mean_length+1)
        for i in range(mean_length):
            Lbl = tk.Label(newWindow, font=("helvetica", "10"))
            Lbl.grid(column=i + 1, row=1)

        for i in range(mean_length):
            Lbl = tk.Label(newWindow, text="Event "+str(i+1)
                           , font=("helvetica", "10"))
            Lbl.grid(column=i+1, row=2)

        top=5
        for i in range(top):
            Lbl = tk.Label(newWindow, text="Top " + str(i + 1)
                           , font=("helvetica", "10"))
            Lbl.grid(column=0, row=3+i)

        for j in range(mean_length):
            k = Counter(cluster.cluster_details["event"+str(j+1)])
            high = k.most_common(top)
            for index,i in enumerate(high):
                Lbl = tk.Label(newWindow,text=i[0]+" "+str(int(i[1]*100/len(cluster.tr)))+"%", font=("helvetica", "10"))
                Lbl.grid(column=j + 1, row=3+index)


    def draw_clusters(self, clusters, removing_outliers=0):
        if str(self.var.get()) == str(1):
            canvas = self.canvas
        else:
            canvas = self.canvas2


        cluster_width = self.CANVAS_WIDTH / 2 - 10

        cluster_height = 120

        p1=(7,7)
        p2=(cluster_width, cluster_height)

        for index, cluster in enumerate(clusters):
            avg_length, outOfOrder, avg_sim, number_of_trajectories, number_of_similar_trajectories, WSS = cluster.cluster_info()
            avg_length2, outOfOrder2, avg_sim2, number_of_trajectories2, number_of_similar_trajectories2 = cluster.cluster_info_without_outliers()

            rect = canvas.create_rectangle(p1, p2, fill="white", tags=(str(index), "clickable"))
            if removing_outliers == 1:
                if (str(self.var.get()) == str(1) and self.similarity_measure.computeDistance(cluster.mean, self.clusters2[index].mean, self.similarity_measure_type) == 0) or (str(self.var.get()) == str(2) and self.similarity_measure.computeDistance(cluster.mean, self.clusters[index].mean, self.similarity_measure_type) == 0):
                    canvas.itemconfig(rect, outline="green")
                else:
                    canvas.itemconfig(rect, outline="red")

            canvas.create_text(p1[0] + cluster_width / 2, p1[1] + cluster_height / 2,
                               text=str(outOfOrder) + "% out of order ("+str(outOfOrder2)+"%)\n"
                                                      "Average length = " + str(int(avg_length)) + " ("+str(int(avg_length2))+")\n"
                                                      "Average distance to the mean = " + str(round(avg_sim, 2)) + " ("+str(round(avg_sim2, 2))+")\n"
                                                      "Number of trajectories = "+str(number_of_trajectories)+" ("+str(number_of_trajectories2)+")\n"
                                                      "Number of trajectories sim to the mean = "+str(number_of_similar_trajectories)+" ("+str(number_of_similar_trajectories2)+")",
                               fill="black", tags=(str(index), "clickable"))
            if index % 3 ==0:
                temp_y = p1[1]
                p1 = (cluster_width + 10,temp_y)
                temp_y = p2[1]
                p2 = (cluster_width*2 + 10 ,temp_y)

            elif index % 3 == 1:
                temp_y = p1[1]
                p1 = (self.CANVAS_WIDTH/3, temp_y + cluster_height + 10)
                temp_y= p2[1]
                p2 = (self.CANVAS_WIDTH/3 + cluster_width, temp_y + cluster_height + 10)
            else:
                temp_y = p1[1]
                p1 = (7, temp_y + cluster_height + 10)
                temp_y = p2[1]
                p2 = (cluster_width, temp_y + cluster_height + 10)




