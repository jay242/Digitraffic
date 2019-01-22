import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import time
import threading
import pprint as pp
from FetchandStore import FetchandStore

class DataFeatures:
    @staticmethod
    def sensortypes(sensors):
        sensornames = [sensor["name"] for sensor in sensors ]
        sensornames = list(set(sensornames))
        for index, sensorname in enumerate(sorted(sensornames)):
            print(index, sensorname)

        measuredtime = [sensor["datetime"] for sensor in sensors ]
        measuredtime = list(set(measuredtime))
    #    for index, measuredtime in enumerate(sorted(measuredtime)):
     #       print(index, measuredtime)


    @staticmethod
    def processdata(sensorName):
        connection = sqlite3.connect('sensordata.db')
        df = pd.read_sql_query("SELECT * FROM sensordata WHERE name = :name ",connection, parse_dates=['TIME'],
                               params={'name': sensorName}, index_col='TIME')
        df =df.sort_index()
        print(df.tail(100))
        df.VALUE.resample('min').mean().plot()
        plt.title('Air temperature in 1 minute intervals for the first 100 sensors')
        plt.xlabel('Time')
        plt.ylabel('Temperature in Degrees')
        plt.show()
        return df

    @staticmethod
    def accumulate(roadstationid):
        sensors = FetchandStore.getData("https://tie.digitraffic.fi/api/v1/data/weather-data")
        roadstationvalues = [sensor for sensor in sensors if sensor["id"] == roadstationid]
       # FetchandStore.storeroaddataindb(roadstationvalues)
        #pp.pprint(roadstationvalues)
        print(time.ctime())
       # pp.pprint(roadstationvalues)
        threading.Timer(10, DataFeatures.accumulate(roadstationid)).start()
