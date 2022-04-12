import psycopg2 as psycopg2
from Classes.trajectory import *

class dbQuerying:


    def __init__(self):
        self.conn = psycopg2.connect(
        "dbname=BNF port=5432 user=postgres password=Postalaa1")


    def getRandomTrajectories(self, dictionaries,table_name='eventstrajectories', out_of_order_percent=30, miminum_length=3, maximum_length=10, out_of_order=1000):

        cursor = self.conn.cursor()
        trajectories_set_ooo=[]
        trajectories_set_communicable = []
        query = "select id_uc, id_events, type_events, class" \
                " from "+table_name+\
                " where class=0 and length >="+str(miminum_length)+" and length <="+str(maximum_length)+" order by random() limit "+str(out_of_order)

        cursor.execute(query)
        for row in cursor:
            tr = trajectory(row[0], row[1], row[2], row[3],dictionaries)
            trajectories_set_ooo.append(tr)

        number_of_outOfOrder=len(trajectories_set_ooo)
        number_of_communicable=int(number_of_outOfOrder*(100-out_of_order_percent)/out_of_order_percent)

        query = "select id_uc, id_events, type_events, communicability" \
                " from " + table_name + \
                " where class=1 and length >=" + str(miminum_length)+" and length <="+str(maximum_length)+" order by random()" \
                "limit "+str(number_of_communicable)
        cursor.execute(query)

        for row in cursor:
            tr = trajectory(row[0], row[1], row[2], row[3], dictionaries)
            trajectories_set_communicable.append(tr)

        return trajectories_set_ooo, trajectories_set_communicable