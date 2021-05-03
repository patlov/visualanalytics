

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
    def __init__(self, timestamp : datetime, pressure :float, altitude :float, pressure_sealevel : float, temperature : float, humidity : float):
        self.timestamp = timestamp
        self.pressure = pressure
        self.altitude = altitude
        self.pressure_sealevel = pressure_sealevel
        self.humidity = humidity
        self.temperature = temperature

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2, ensure_ascii=False)


class Sensor:
    def __init__(self, id : int, type : SensorType, location : int, lat : float, long : float):
        self.id = id
        self.type = type
        self.location = location
        self.long = long
        self.lat = lat
        self.dataList = []

    def addDatapoint(self, datapoint : SensorData):
        self.dataList.append(datapoint)


    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2, ensure_ascii=False)



