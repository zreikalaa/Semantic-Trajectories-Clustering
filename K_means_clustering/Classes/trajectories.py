from Classes.trajectory import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go
import numpy as np
class trajectories:
    def __init__(self):
        self.trajectoriesSet=[]

    def createTrajectories(self,cursor):
        query = "select * " \
                "from trajectories " \
                "where (communicabilite=0 or communicabilite=2 or communicabilite=13) and length between 30 and 100" \
                "order by random() " \
                "limit 1000"
        cursor.execute(query)

        for row in cursor:
            tr = trajectory(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
            tr.generateTrajectory()
            self.trajectoriesSet.append(tr)
        return self.trajectoriesSet

    def print(self):
        for idx, tr in enumerate(self.trajectoriesSet):
            tr.print()
            print(idx,"\n")

    def analyseLength(self,cursor):
        query ="select length,count(*) from trajectories group by length having length<100 and length>50 order by length"
        cursor.execute(query)
        x = []
        y = []
        for row in cursor:
            x.append(row[0])
            y.append(row[1])
            print(row[0], ":", row[1])
        plt.xlabel('trajectories length')
        plt.ylabel('nomber of document')
        plt.plot(x, y)
        plt.show()

    def analyseCommunicationRate(self,cursor):
        query="select communication,count(*) from(select events.id_uc,count(*) as communication from events,trajectories where type_event=3 and events.id_uc=trajectories.id_uc group by events.id_uc)as d group by communication having communication between 50 and 100 order by communication"
        cursor.execute(query)
        x = []
        y = []
        for row in cursor:
            x.append(row[0])
            y.append(row[1])
            print(row[0], ":", row[1])
        plt.xlabel('number of communication')
        plt.ylabel('number of document')
        plt.plot(x, y)
        query = "select length,count(*) from trajectories group by length having length between 50 and 100 order by length"
        cursor.execute(query)
        for idx,row in enumerate(cursor):
            if y[idx]<row[1]:
                y[idx]=row[1]
        red_patch = mpatches.Patch(color='red', label='All events')
        blue_patch = mpatches.Patch(color='blue', label='communication')
        plt.legend(handles=[blue_patch,red_patch])
        plt.xlabel('trajectories length')
        plt.ylabel('number of document')
        plt.plot(x, y)
        plt.show()
    def analyseLengthAndCommunicability(self,cursor):
        x1 = []
        x2 = []
        y = []
        query = "select length,count(*) from trajectories where communicabilite=2 group by length having length<500 and length>50 order by length"
        cursor.execute(query)
        for row in cursor:
            x1.append(row[1])
            y.append(row[0])

        query = "select length,count(*) from trajectories where communicabilite=0 or communicabilite=13 group by length having length<500 and length>50 order by length"
        cursor.execute(query)
        for row in cursor:
            x2.append(row[1])

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=y,
            x=x1,
            name='communicable',
            orientation='h',
            marker=dict(
                color='rgba(246, 78, 139, 0.6)',
                line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
            )
        ))
        fig.add_trace(go.Bar(
            y=y,
            x=x2,
            name='out of order',
            orientation='h',
            marker=dict(
                color='rgba(58, 71, 80, 0.6)',
                line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
            )
        ))

        fig.update_layout(barmode='stack')
        fig.show()



