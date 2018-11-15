from FetchandStore import FetchandStore
from DataFeatures import DataFeatures

class WeatherStationData:
    #def __init__(self,weatherStationId, roadStationId, name,sensorValue,sensorUnit):

    def __init__(self):
        pass
       # self.weatherStationId = weatherStationId
       # self.roadStationId = roadStationId
       # self.name = name
       # self.sensorValue = sensorValue
       # self.sensorUnit = sensorUnit
#
    fs = FetchandStore()
    df = DataFeatures()
#temp = WeatherStationData(1,2048,"stn",0.0, "deg")
temp = WeatherStationData()

#temp.fs.datatoseries(temp.fs.fetchdatafromdb('airtemperature1'))
temp.df.sensortypes(temp.fs.getData("https://tie.digitraffic.fi/api/v1/data/weather-data"))