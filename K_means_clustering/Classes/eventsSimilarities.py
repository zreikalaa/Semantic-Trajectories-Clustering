from Classes.event import *
from Classes.communication import *
from Classes.treatment import *
from Classes.degradation import *
from Classes.refusedcommunication import *
import rdflib
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery


class eventsSimilarities:

    def __init__(self):
        self.graph = rdflib.Graph()
        self.graph.parse("dalgology.owl")
        self.equivalencceValue = 1
        self.inclusionValue = 0.8
        self.commonHeritanceValue = 0.5
        self.generalConcepts = ["http://www.semanticweb.org/Dalgology#Traitement",
                                "http://www.semanticweb.org/Dalgology#Dégradation",
                                "http://www.semanticweb.org/Dalgology#événement"]

    def getEquivalentEventsById(self, eventId):
        toSearch = [eventId]
        allEvents = [eventId]
        while len(toSearch) > 0:
            firstEvent = toSearch[0]
            del toSearch[0]
            q = prepareQuery('''SELECT ?id2 WHERE { ?a <http://www.semanticweb.org/Dalgology#Id> ?id .
                     {?b <http://www.w3.org/2002/07/owl#equivalentClass> ?a} UNION {?a <http://www.w3.org/2002/07/owl#equivalentClass> ?b}.
                     ?b <http://www.semanticweb.org/Dalgology#Id> ?id2.
                     FILTER (?id="''' + firstEvent + '''"^^xsd:string) }''')
            for row in self.graph.query(q):
                if row[0].toPython() not in allEvents:
                    allEvents.append(row[0].toPython())
                    toSearch.append(row[0].toPython())
        return allEvents


    def equivalenceSimilarity(self, event1, event2):
        if event1.id_event == event2.id_event:
            return 1
        # Search all the equivalent events to event1 and stock them in 'AllEvents' array---------------------------------
        equivalentToEvent1 = self.getEquivalentEventsById(event1.id_event)
        # ---------------------------------------------------------------------------------------------------------------
        if event2.id_event in equivalentToEvent1:
            return 1
        return 0


    def getParentsOfEventName(self, eventName):
        toSearch = [eventName]
        eventParents = []
        while len(toSearch) > 0:
            firstEvent = toSearch[0]
            del toSearch[0]
            try:
                q = prepareQuery('''SELECT ?parent WHERE { <''' + firstEvent + '''> rdfs:subClassOf ?parent .}''')
            except: print(firstEvent)
            for row in self.graph.query(q):
                if row[0].toPython() not in eventParents:
                    eventParents.append(row[0].toPython())
                    toSearch.append(row[0].toPython())
        return eventParents


    def getEventNameById(self, eventId):
        q = prepareQuery('''SELECT ?a WHERE { ?a <http://www.semanticweb.org/Dalgology#Id> ?id .
                                         FILTER (?id="''' + eventId + '''"^^xsd:string) }''')
        for row in self.graph.query(q):
            return row[0].toPython()
        return None


    def inclusionSimilarity(self, event1, event2):
        # The search will be by name and not by id because some concepts are not real events(they are created only to
        # group similar events)
        # We need to get the name of the two events
        event1Name = self.getEventNameById(event1.id_event)
        event2Name = self.getEventNameById(event2.id_event)
        # Search all the parents of event1 and event2 and stock them in event1Parents and event2Parents-----------------
        try:
            event1Parents = self.getParentsOfEventName(event1Name)
            event2Parents = self.getParentsOfEventName(event2Name)
        except:
            print("event id=",event1.id_event," event name=", self.getEventNameById(event1.id_event))
            print("event id=", event2.id_event, " event name=", self.getEventNameById(event2.id_event))
        if event1Name in event2Parents or event2Name in event1Parents:
            return 1


    def intersectionTwoArrays(self, array1, array2):
        intersection = []
        for item1 in array1:
            for item2 in array2:
                if item1 == item2:
                    intersection.append(item1)
        return intersection


    def arrayInTheAnother(self, array1, array2):  # return 1 if array2 in array1, 0 otherwise......
        found = 0
        for item2 in array2:
            for item1 in array1:
                if item1 == item2:
                    found = 1
                    break
            if found == 0:
                return 0
            found = 0
        return 1


    def commonHeritanceSimilarity(self, event1, event2):
        # get the parents of the two events
        event1Name = self.getEventNameById(event1.id_event)
        event2Name = self.getEventNameById(event2.id_event)
        event1Parents = self.getParentsOfEventName(event1Name)
        event2Parents = self.getParentsOfEventName(event2Name)
        # get the common parents
        intersection = self.intersectionTwoArrays(event1Parents, event2Parents)
        # check if we have a not general common parent
        return not self.arrayInTheAnother(self.generalConcepts, intersection)


    def compute(self, event1, event2):
        if self.equivalenceSimilarity(event1, event2):
            return self.equivalencceValue
        elif self.inclusionSimilarity(event1, event2):
            return self.inclusionValue
        elif self.commonHeritanceSimilarity(event1, event2):
            return self.commonHeritanceValue
        else:
            return 0