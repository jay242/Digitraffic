import requests as re
import csv
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import  pprint as pp


class FetchandStore:
    sensors = []
    sensordict = {}

    @staticmethod
    def get_data(link):
        """Fetches weatherstation data from the link provided and extracts sensor readings across all
        weatherstations into a dictionary of lists of dictionaries"""
        data = re.get(link)
        jsondata = data.json()
        for weatherstation in jsondata['weatherStations']:
            FetchandStore.sensordict.update({weatherstation["id"]:weatherstation["sensorValues"]})
            for sensorvalue in weatherstation["sensorValues"]:
                FetchandStore.sensors.append({"id": sensorvalue["roadStationId"], "name": sensorvalue["oldName"],
                                              "value": sensorvalue["sensorValue"], "unit": sensorvalue["sensorUnit"],
                                              "datetime": sensorvalue["measuredTime"]})
        return FetchandStore.sensors

    @staticmethod
    def store_data_in_db(sensors):
        """Stores the sensor readings in an SQLite database. Data stored are roadstation id, sensor name, measured value, unit
        and the time at which the measurements were takem"""
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
    def fetch_data_from_db(sensorName):
        """Fetches the sensor measurements from db and returns it as a string"""
        connection = sqlite3.connect('sensordata.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sensordata WHERE name = :name", {'name': sensorName})
        observedsensor = cursor.fetchall()
        return observedsensor

    @staticmethod
    def dbtocsv():
        """Method to fetch data from db and populate a csv file with it"""
        connection = sqlite3.connect("sensordata.db")
        cursor = connection.cursor()
        cursor.execute("Select * from sensordata")
        roadstationdata = cursor.fetchall()

        with open('roadstationdata.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id','name','value','unit','time'])
            writer.writerows(roadstationdata)

# make one sensor reading as the dependent variable. All other sensors independent variable. Create columns like that.


class DataFeatures:
    @staticmethod
    def sensor_types():
        """Prints the list of sensors that are part of this measurement"""
        sensors = FetchandStore.get_data("https://tie.digitraffic.fi/api/v1/data/weather-data")
        sensornames = [sensor["name"] for sensor in sensors ]
        sensornames = list(set(sensornames))
        for index, sensorname in enumerate(sorted(sensornames)):
            print(index, sensorname)

    @staticmethod
    def process_data(sensorName):
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
    def find_relation(sensors):
        """Takes any two sensors, finds the roadstations in which they are both present and compares their
        correlation by means of a plot """
        sensor1name = "humidity"
        sensor2name = "roadsurfacetemperature1"
        sensor1val = {}
        sensor2val = {}

        for sensor in sensors:
            if sensor1name == sensor["name"]:
                sensor1val.update({sensor["id"]:sensor["value"]})
                sensor1unit = sensor["unit"]
            elif sensor2name == sensor["name"]:
                sensor2val.update({sensor["id"]:sensor["value"]})
                sensor2unit = sensor["unit"]

        var1 = []
        var2 = []

        for key in set(sensor1val).intersection(set(sensor2val)):
            var1.append(sensor1val[key])
            var2.append(sensor2val[key])

        plt.scatter(var1, var2)
        plt.title(sensor1name + " vs " + sensor2name)
        plt.xlabel(sensor1name + " ( " + sensor1unit + " )")
        plt.ylabel(sensor2name + " ( " + sensor2unit + " )")
        plt.show()

        return var1, var2

    @staticmethod
    def extract_sensor_data(features, target):
        X = {key: [] for key in features}
        y = []
        for sensor in FetchandStore.sensors:
            for feature in features:
                if sensor["name"] == feature:
                    X[feature].append(sensor["value"])
                elif sensor["name"] == target:
                    y.append(sensor["value"])

        # pp.pprint(y)
        return X, y

    @staticmethod
    def extract_sensor_data_to_csv(features, target):
        with open("sensordata.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerow(features)
            for sensor in FetchandStore.sensors:
                X = [sensor["value"] for feature in features if feature == sensor["name"]]
                pp.pprint(X)
                writer.writerow(X)


class UserInterface:

    @staticmethod
    def show_sensor_list():
        choice = str(input("Would you like to see the list of available sensors?(Y/N)"))
        if choice.upper() == 'Y':
            DataFeatures.sensor_types()

    @staticmethod
    def choose_sensors():
        ind = [i for i in input("Enter the independent variable names separated by commas: ").split(',')]
        print("These are the variables you chose: ", ind)
        target = input("Enter the dependent variable name: ")
        print("This is the target variables you chose: ", target)
        DataFeatures.extract_sensor_data_to_csv(ind, target)


FetchandStore.get_data("https://tie.digitraffic.fi/api/v1/data/weather-data")

# FetchandStore.store_data_in_db(FetchandStore.sensors)

# Plot the first 100 values of the given sensor against time
# DataFeatures.sensortypes(FetchandStore.sensors)

# Find the relation between any two sensor types by plotting the values against each other.
#DataFeatures.find_relation(FetchandStore.sensors)

UserInterface.choose_sensors()