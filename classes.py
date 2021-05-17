

import datetime
from enum import Enum
import json
import pandas as pd

# sensor types : bme280 bmp180 ssds011 dht22

class SensorType(str, Enum):
    bme280: str = "bme280"
    bmp180: str = "bmp180"
    ssds011: str = "ssds011"
    dht22: str = "dht22"



class Sensor:
    def __init__(self, id : int, type : SensorType, country : str, state : str, city : str, lat : float, long : float):

        if id != '':
            self.id = int(id)
        else:
            self.id = 'NA'

        self.type = type

        self.country = country
        self.state = state
        self.city = city


        if long != '':
            self.long = float(long)
        else:
            self.long = 'NA'

        if lat != '':
            self.lat = float(lat)
        else:
            self.lat = 'NA'

        self.dataFrame = pd.DataFrame()

    def addDatapoint(self, timestamp : datetime, pressure :float, altitude, pressure_sealevel, temperature : float, humidity : float):
        row = {'timestamp':timestamp, 'pressure':pressure, 'altitude':altitude, 'pressure_sealevel':pressure_sealevel, 'temperature':temperature, 'humidity': humidity}
        self.dataFrame = self.dataFrame.append(row, ignore_index=True)
        pass

    def addDatapoints(self, rows):
        self.dataFrame = self.dataFrame.append(rows, ignore_index=True)
        pass


    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2, ensure_ascii=False)



