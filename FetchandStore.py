import requests as re
import sqlite3
import pandas as pd
import pprint

class FetchandStore:

    def getData(self, link):
        self.link = link
        data = re.get(link)
        jsondata = data.json()

        for weatherstation in jsondata['weatherStations']:
            sensors = [{"id": sensorvalue["roadStationId"], "name": sensorvalue["oldName"],
                    "value": sensorvalue["sensorValue"], "unit": sensorvalue["sensorUnit"],
                    "datetime":sensorvalue["measuredTime"]} for sensorvalue in weatherstation["sensorValues"]]
        return sensors

    def storedataindb(self, sensors):
        connection = sqlite3.connect('sensordata.db')
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS sensordata (
                        ID int, NAME text, VALUE real, UNIT text, TIME text )"""
                       )
        with connection:
            for sensor in sensors:
                cursor.execute("INSERT INTO sensordata VALUES (:id, :name, :value, :unit, :time)",
                               {'id':sensor['id'], 'name':sensor['name'],
                                'value':sensor['value'], 'unit': sensor['unit'], 'time':sensor['datetime']})

    def fetchdatafromdb(self,sensorName):
        connection = sqlite3.connect('sensordata.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sensordata WHERE name = :name", {'name': sensorName})
        observedsensor = cursor.fetchall()
        return observedsensor

    def datatoseries(self, observedsensor):
        #timedata = []
        #index = []
        #for i in observedsensor:
         #   timedata.append(i[2])
        #    index.append(i[4])
        timedata = [sensor[2] for sensor in observedsensor]
        index = [sensor[4] for sensor in observedsensor]
        data = pd.Series(timedata, index=pd.DatetimeIndex(index))
        # pprint.pprint(pd.DatetimeIndex(index1))
        pprint.pprint(data)
       # data.plot.bar()
       # plt.show()