from Classes.event import *
from Classes.communication import *
from Classes.treatment import *
from Classes.degradation import *
from Classes.refusedcommunication import *
import rdflib
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from Classes.eventsSimilarities import *


class LCESSSim:
    def __init__(self, dictionaries, ontology_depth):

        self.dictionaries = dictionaries
        self.ontology_depth = ontology_depth

        self.equivalent_similarity = 1
        self.similar_communication = 0.5
        self.alpha = 0.7

    def Head(self, trajectory):
        if len(trajectory) > 0:
            return trajectory[0]
        return None

    def inclusion(self, length):
        return 1 - (1 - self.alpha) * (length / self.ontology_depth)

    def closeness(self, length1, length2):
        return self.alpha - (self.alpha * ((length1 + length2) / (2 * self.ontology_depth)))

    def Rest(self, trajectory):
        if len(trajectory) > 0:
            return trajectory[1:]
        return None

    def events_similarity(self, event_1, event_2):

        if isinstance(event_1, communication) and isinstance(event_2, communication):
            if event_1.level == event_2.level:
                return self.equivalent_similarity
            else:
                return self.similar_communication

        if isinstance(event_1, refusedcommunication) and isinstance(event_2, refusedcommunication):
            if event_1.level == event_2.level:
                return self.equivalent_similarity
            else:
                return self.similar_communication

        if (isinstance(event_1, treatment) and isinstance(event_2, treatment)) or (
                isinstance(event_1, degradation) and isinstance(event_2, degradation)):
            event1_name = self.dictionaries["class name of id " + event_1.id_event]
            event2_name = self.dictionaries["class name of id " + event_2.id_event]
            dic1 = self.dictionaries["equivalent to " + event_1.id_event]
            dic2 = self.dictionaries["equivalent to " + event_2.id_event]
            if event_1.id_event == event_2.id_event or event_1.id_event in self.dictionaries[
                "equivalent to " + event_2.id_event] \
                    or event_2.id_event in self.dictionaries["equivalent to " + event_1.id_event]:
                return self.equivalent_similarity

            elif event1_name in self.dictionaries[str(event_2.id_event)].keys():

                return self.inclusion(int(self.dictionaries[str(event_2.id_event)][event1_name]))

            elif event2_name in self.dictionaries[str(event_1.id_event)].keys():
                return self.inclusion(int(self.dictionaries[str(event_1.id_event)][event2_name]))

            else:
                nearest_parent_distance = self.ontology_depth
                length1 = 0
                length2 = 0
                for parent in self.dictionaries[str(event_1.id_event)].keys():
                    if parent in self.dictionaries[str(event_2.id_event)].keys():
                        if self.dictionaries[str(event_1.id_event)][parent] + self.dictionaries[str(event_2.id_event)][
                            parent] < nearest_parent_distance:
                            length1 = self.dictionaries[str(event_1.id_event)][parent]
                            length2 = self.dictionaries[str(event_2.id_event)][parent]

                    return self.closeness(length1, length2)
        return 0

    def lcess(self, events_sequence_1, events_sequence_2):
        if len(events_sequence_1) == 0 or len(events_sequence_2) == 0:
            return 0

        sim = self.events_similarity(self.Head(events_sequence_1), self.Head(events_sequence_2))

        if sim == 1:
            return self.lcess(self.Rest(events_sequence_1), self.Rest(events_sequence_2)) + 1
        elif sim > 0:
            '''return max(self.lcess(self.Rest(events_sequence_1), self.Rest(events_sequence_2)) + sim,
                       self.lcess(self.Rest(events_sequence_1), events_sequence_2),
                       self.lcess(events_sequence_1, self.Rest(events_sequence_2))
                       )'''
            return self.lcess(self.Rest(events_sequence_1), self.Rest(events_sequence_2)) + sim
        else:
            return max(self.lcess(events_sequence_1, self.Rest(events_sequence_2)),
                       self.lcess(self.Rest(events_sequence_1), events_sequence_2))

    def computeDistance(self, trajectory1, trajectory2, similarity_measure_type):
        try:
            if similarity_measure_type=="LCESS":
                lcess = self.lcess(trajectory1.events, trajectory2.events)
                sim = lcess / ((len(trajectory1.events) + len(trajectory2.events)) - lcess)
            elif similarity_measure_type=="LCSS":
                lcss = self.lcss(trajectory1.events, trajectory2.events)
                sim = lcss / ((len(trajectory1.events) + len(trajectory2.events)) - lcss)
        except KeyError as e:
            sim = 0

        return 1 - sim

    def lcss(self, events_sequence_1, events_sequence_2):
        if len(events_sequence_1) == 0 or len(events_sequence_2) == 0:
            return 0

        event_1 = self.Head(events_sequence_1)
        event_2 = self.Head(events_sequence_2)

        if isinstance(event_1, communication) and isinstance(event_2, communication) and event_1.level == event_2.level:
            return self.lcss(self.Rest(events_sequence_1), self.Rest(events_sequence_2)) + 1

        elif isinstance(event_1, refusedcommunication) and isinstance(event_2, refusedcommunication) and event_1.level == event_2.level:
            return self.lcss(self.Rest(events_sequence_1), self.Rest(events_sequence_2)) + 1

        elif ((isinstance(event_1, treatment) and isinstance(event_2, treatment)) or (isinstance(event_1, degradation) and isinstance(event_2,degradation)))\
                and event_1.id_event == event_2.id_event:
            return self.lcss(self.Rest(events_sequence_1), self.Rest(events_sequence_2)) + 1

        else:
            return self.lcss(self.Rest(events_sequence_1), self.Rest(events_sequence_2))
