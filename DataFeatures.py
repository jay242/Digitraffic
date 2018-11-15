import pprint
class DataFeatures:
    def sensortypes(self,sensors):
        sensornames = [sensor["name"] for sensor in sensors ]
        sensornames = list(set(sensornames))
        pprint.pprint(sorted(sensornames))