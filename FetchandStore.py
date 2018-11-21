import requests as re
import sqlite3

class FetchandStore:

    @staticmethod
    def getData(link):
        data = re.get(link)
        jsondata = data.json()
        sensors =[]
        for weatherstation in jsondata['weatherStations']:
            for sensorvalue in weatherstation["sensorValues"]:
                sensors.append({"id": sensorvalue["roadStationId"], "name": sensorvalue["oldName"],
                                   "value": sensorvalue["sensorValue"], "unit": sensorvalue["sensorUnit"],
                                   "datetime":sensorvalue["measuredTime"]})
        return sensors

    @staticmethod
    def storedataindb(sensors):
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
    @staticmethod
    def fetchdatafromdb(sensorName):
        connection = sqlite3.connect('sensordata.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sensordata WHERE name = :name", {'name': sensorName})
        observedsensor = cursor.fetchall()
        return observedsensor

