

import datetime
from enum import Enum
import json

# sensor types : bme280 bmp180 ssds011 dht22

class SensorType(str, Enum):
    bme280: str = "bme280"
    bmp180: str = "bmp180"
    ssds011: str = "ssds011"
    dht22: str = "dht22"



class SensorData:
    def __init__(self, timestamp : datetime, pressure :float, altitude, pressure_sealevel, temperature : float, humidity : float):


        self.timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")

        if pressure != '':
            self.pressure = float(pressure)
        else:
            self.pressure = 'NA'

        if altitude != '':
            self.altitude = float(altitude)
        else:
            self.altitude = 'NA'

        if pressure_sealevel != '':
            self.pressure_sealevel = float(pressure_sealevel)
        else :
            self.pressure_sealevel = 'NA'

        if humidity != '':
            self.humidity = float(humidity)
        else:
            self.humidity = 'NA'

        if temperature != '':
            self.temperature = float(temperature)
        else:
            self.temperature = 'NA'

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2, ensure_ascii=False)


class Sensor:
    def __init__(self, id : int, type : SensorType, location : int, lat : float, long : float):

        if id != '':
            self.id = int(id)
        else:
            self.id = 'NA'

        self.type = type

        if location != '':
            self.location = int(location)
        else:
            self.location = 'NA'

        if long != '':
            self.long = float(long)
        else:
            self.long = 'NA'

        if lat != '':
            self.lat = float(lat)
        else:
            self.lat = 'NA'

        self.dataList = []

    def addDatapoint(self, datapoint : SensorData):
        self.dataList.append(datapoint)


    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2, ensure_ascii=False)



