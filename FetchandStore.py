import requests as re
import sqlite3
import  csv

class FetchandStore:
    sensors = []

    # @staticmethod
    def getData(link):
        data = re.get(link)
        jsondata = data.json()
        for weatherstation in jsondata['weatherStations']:
            for sensorvalue in weatherstation["sensorValues"]:
                FetchandStore.sensors.append({"id": sensorvalue["roadStationId"], "name": sensorvalue["oldName"],
                                              "value": sensorvalue["sensorValue"], "unit": sensorvalue["sensorUnit"],
                                              "datetime": sensorvalue["measuredTime"]})
        return FetchandStore.sensors

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
                               {'id': sensor['id'], 'name': sensor['name'],
                                'value': sensor['value'], 'unit': sensor['unit'], 'time': sensor['datetime']})

    @staticmethod
    def fetchdatafromdb(sensorName):
        connection = sqlite3.connect('sensordata.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sensordata WHERE name = :name", {'name': sensorName})
        observedsensor = cursor.fetchall()
        return observedsensor

    def storeroaddataindb(roadstationvalues):
        connection = sqlite3.connect('roadstation.db')
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS roadstation (
                        ID int, NAME text, VALUE real, UNIT text, TIME text )"""
                       )
        with connection:
            for roadstation in roadstationvalues:
                cursor.execute("INSERT INTO roadstation VALUES (:id, :name, :value, :unit, :time)",
                               {'id': roadstation['id'], 'name': roadstation['name'],
                                'value': roadstation['value'], 'unit': roadstation['unit'],
                                'time': roadstation['datetime']})
                connection.commit()

                #connection.close()

    @staticmethod
    def dbtocsv():
        connection = sqlite3.connect("roadstation.db")
        cursor = connection.cursor()
        cursor.execute("Select * from roadstation")
        roadstationdata = cursor.fetchall()

        with open('roadstationdata.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id','name','value','unit','time'])
            writer.writerows(roadstationdata)

#make one sensor readig as the dependent variable. All other sensors independent variable. Create columns like that.