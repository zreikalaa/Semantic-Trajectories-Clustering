import threading
import time
import rdflib
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph
from sklearn.cluster import DBSCAN
import matplotlib.animation as animation
from matplotlib import style
import psycopg2 as psycopg2
import time
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
import numpy as np

class ontologyQuerying:
    def __init__(self, ontology):
        self.ontology = ontology
        self.dictionaries={}

    def initialize_dictionaries(self):
        graph = rdflib.Graph()
        graph.parse(self.ontology)
        distance = 0
        q = prepareQuery('''select ?id ?a { 
                ?a a <http://www.w3.org/2002/07/owl#Class>.
                ?a <http://www.semanticweb.org/Dalgology#Id> ?id .}''')
        for row in graph.query(q):
            self.dictionaries[str(row[0])]={}

            self.dictionaries["equivalent to "+str(row[0])] = []
            self.dictionaries["class name of id "+str(row[0])] = str(row[1])

        q = prepareQuery('''select ?id (count(?mid) as ?distance) ?b { 
                    ?a <http://www.semanticweb.org/Dalgology#Id> ?id .
                    ?a rdfs:subClassOf* ?mid .
                    ?mid rdfs:subClassOf+ ?b .
                    } group by ?a ?b''')

        ontology_depth = 0
        for row in graph.query(q):
            if ontology_depth < int(row[1]):
                ontology_depth = int(row[1])

        for row in graph.query(q):
            if ontology_depth-1 > int(row[1]):
                self.dictionaries[str(row[0])][str(row[2])]=int(row[1])

        q = prepareQuery('''select ?id1 ?id2 { 
                           ?a <http://www.w3.org/2002/07/owl#equivalentClass> ?b .
                           ?a <http://www.semanticweb.org/Dalgology#Id> ?id1.
                           ?b <http://www.semanticweb.org/Dalgology#Id> ?id2
                           } ''')

        for row in graph.query(q):
            self.dictionaries["equivalent to "+str(row[0])].append(str(row[1]))

        return ontology_depth, self.dictionaries




