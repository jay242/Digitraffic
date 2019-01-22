from FetchandStore import FetchandStore
from DataFeatures import DataFeatures

#Fetch the data from digitraffic website, parse the json and store relevant values in database
#FetchandStore.storedataindb(FetchandStore.getData("https://tie.digitraffic.fi/api/v1/data/weather-data"))
# Plot the first 100 values of the given sensor against time
#DataFeatures.sensortypes(FetchandStore.sensors)
#DataFeatures.processdata('airtemperature1')
#DataFeatures.accumulate(3073)
FetchandStore.dbtocsv()