import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


class DataFeatures:
    @staticmethod
    def sensortypes(sensors):
        sensornames = [sensor["name"] for sensor in sensors ]
        sensornames = list(set(sensornames))
        for index, sensorname in enumerate(sorted(sensornames)):
            print(index, sensorname)

    @staticmethod
    def processdata(sensorName):
        connection = sqlite3.connect('sensordata.db')
        df = pd.read_sql_query("SELECT * FROM sensordata WHERE name = :name limit 100",connection, parse_dates=['TIME'],
                               params={'name': sensorName}, index_col='TIME')
        df =df.sort_index()
        df.VALUE.resample('1T').mean().plot()
        plt.title('Air temperature in 1 minute intervals for the first 100 sensors')
        plt.xlabel('Time')
        plt.ylabel('Temperature in Degrees')
        plt.show()
        return df
