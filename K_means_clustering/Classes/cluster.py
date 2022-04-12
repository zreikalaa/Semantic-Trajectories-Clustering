from Classes.event import *
from Classes.treatment import *
from Classes.communication import *
from Classes.degradation import *
from Classes.refusedcommunication import *
from Classes.trajectory import *
class cluster:


    def __init__(self, mean, dictionaries, threeshold, trajectories = None, similarities = None):
        super().__init__()
        if trajectories is None:
            trajectories = []
        if similarities is None:
            similarities = []
        """
            Mean : the mean of the cluster, type = trajectory
            Trajectories : the trajectories belonging to the cluster, type = list
            Similarities : the similarities between the trajectories and the mean, type = list ... Ex: similarities[i] correspond to the similarity between trajectories[i] and the mean (Value between 0 and 1).   
        """
        self.threeshold = threeshold
        self.dictionaries = dictionaries
        self.tr = trajectories # A list of tuple (trajectory, distance to the mean)
        self.mean=mean
        self.cluster_details={}

    def cluster_info(self):
        """
        :return: The average length of the trajectories
                 The percentage of the out of order trajectories
                 The average distance to the mean
                 The Number of trajectories
                 Number of trajectories having a distance with the mean <= threeshold
                 WSS
        """
        number_of_trajectories = len(self.tr)
        number_of_outoforder = 0
        number_of_similar_trajectories = 0
        length = 0
        WSS=0

        for trajectory_info in self.tr:
            tr = trajectory_info[0]
            distance_to_the_mean = trajectory_info[1]

            # ------------- Count the number of OOO ------------------
            if tr.communicability == 0:
                number_of_outoforder += 1
            # --------------------------------------------------------

            # ------ Count the similar trajectories to the mean ------
            if distance_to_the_mean <= self.threeshold:
                number_of_similar_trajectories += 1
            # --------------------------------------------------------

            # ------------- Sum of the trajectories length -----------
            length += len(tr.events)

            # --------------------------------------------------------
            WSS += distance_to_the_mean

        if length == 0:
            return 0,0,0,0,0,0

        self.percentOOO= int(number_of_outoforder*100/number_of_trajectories)
        return int(length / number_of_trajectories), int(number_of_outoforder*100/number_of_trajectories), \
               WSS / number_of_trajectories, number_of_trajectories, number_of_similar_trajectories, WSS


    def cluster_info_without_outliers(self):
        """
        :return: The average length of the trajectories
                 The percentage of the out of order trajectories
                 The average similarity with the mean
                 The Number of trajectories
                 Number of trajectories having a similaity with the mean >= threeshold
        """
        number_of_trajectories = 0
        number_of_outoforder = 0
        number_of_similar_trajectories = 0
        length = 0
        distances_to_the_mean = 0

        for trajectory_info in self.tr:
            tr = trajectory_info[0]
            distance_to_the_mean = trajectory_info[1]
            if distance_to_the_mean <= self.threeshold:
                number_of_similar_trajectories += 1
                # ------------- Count the number of OOO ------------------
                if tr.communicability == 0:
                    number_of_outoforder += 1
                # --------------------------------------------------------

                # ------------- Sum of the trajectories length -----------
                number_of_trajectories += 1
                length += len(tr.events)
                # --------------------------------------------------------
                distances_to_the_mean += distance_to_the_mean

        if length == 0:
            return 0,0,0,0,0

        return int(length / number_of_trajectories), int(number_of_outoforder*100/number_of_trajectories), \
               distances_to_the_mean/number_of_trajectories, number_of_trajectories, number_of_similar_trajectories


    def cluster_homogeneity(self):
        events = {}
        for trajectory in self.tr:
            for event in trajectory.events:
                if event in events.keys():
                    events[event] += 1
                else:
                    events[event] = 0
        return len(events.keys())


    def update_mean(self):
        if len(self.tr) == 0:
            return
        avg_length = 0
        for trajectory_info in self.tr:
            tr=trajectory_info[0]
            avg_length += len(tr.events)
        avg_length = int(avg_length / len(self.tr))
        #self.cluster_details["avg_length"] = int(avg_length)


        for i in range(int(avg_length)):
            self.cluster_details["event"+str(i+1)] = {}

        for trajectory_info in self.tr:
            tr=trajectory_info[0]
            for index in range(min(avg_length, len(tr.events))):
                if isinstance(tr.events[index], treatment):
                    if "treatment,"+tr.events[index].id_event in self.cluster_details["event"+str(index+1)].keys():
                        self.cluster_details["event"+str(index+1)]["treatment,"+tr.events[index].id_event]+=1
                    else : self.cluster_details["event"+str(index+1)]["treatment,"+tr.events[index].id_event]=1

                elif isinstance(tr.events[index], degradation):
                    if "degradation," + tr.events[index].id_event in self.cluster_details["event" + str(index + 1)].keys():
                        self.cluster_details["event" + str(index + 1)]["degradation," + tr.events[index].id_event] += 1
                    else:
                        self.cluster_details["event" + str(index + 1)]["degradation," + tr.events[index].id_event] = 1

                elif isinstance(tr.events[index], communication):
                    if "communication," + tr.events[index].level in self.cluster_details["event" + str(index + 1)].keys():
                        self.cluster_details["event" + str(index + 1)]["communication," + tr.events[index].level] += 1
                    else:
                        self.cluster_details["event" + str(index + 1)]["communication," + tr.events[index].level] = 1
                elif isinstance(tr.events[index], refusedcommunication):
                    if "refuscommunication," + tr.events[index].level in self.cluster_details["event" + str(index + 1)].keys():
                        self.cluster_details["event" + str(index + 1)]["refuscommunication," + tr.events[index].level] += 1
                    else:
                        self.cluster_details["event" + str(index + 1)]["refuscommunication," + tr.events[index].level] = 1
        events=[]
        type_events=[]
        for i in range(int(avg_length)):
            max = 0
            event = ""
            for key in self.cluster_details["event" + str(i + 1)].keys():
                if self.cluster_details["event" + str(i + 1)][key] > max:
                    max = self.cluster_details["event" + str(i + 1)][key]
                    event = key
            type,id=event.split(",")
            type_events.append(type)
            if type=="refuscommunication" or type =="communication":
                if id=="low":
                    events.append(1)
                elif id=="medium":
                    events.append(4)
                elif id=="high":
                    events.append(7)
            else:
                events.append(id[1:])
        self.mean = trajectory(0, events, type_events, 0, self.dictionaries)


    def removing_outliers(self):
        tr = [i for i in self.tr if i[1] >= self.threeshold]
        return tr


