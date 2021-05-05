
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import *
import csv
import json
from classes import *

local_path = "database/"
base_url = "http://archive.sensor.community/"
ext = "csv"
sensors_path = "database/sensors.json"

def getSensorType(sensor_id):
    if isinstance(sensor_id, int):
        sensor_id = str(sensor_id)
    with open(sensors_path, "r") as jsonFile:
        data = json.load(jsonFile)

    if sensor_id not in data:
        print("error, sensor " + str(sensor_id) + " is not in list")
        return

    return data[sensor_id]


def getCSVContent(file_url):
    print(file_url)
    req = requests.get(file_url)
    content = req.content.decode('utf-8')
    return content


def buildCSVurl(sensor_id, sensor_type, day):
    return base_url + day + "/" + buildFilename(sensor_id, sensor_type, day) + ".csv"


def buildFilename(sensor_id, sensor_type, day):
    return day + "_" + str(sensor_type) + "_sensor_" + str(sensor_id)


def firstLineValid(header):
    if header[0] != 'sensor_id' or header[1] != 'sensor_type' or header[2] != 'location' \
            or header[3] != 'lat' or header[4] != 'lon' or header[5] != 'timestamp':
        return False

    if header[6] != 'pressure' or header[7] != 'altitude' or header[8] != 'pressure_sealevel' or \
        header[9] != 'temperature' or header[10] != 'humidity':
        return False

    return True


def getDataOfOneDay(sensor_id, sensor_type, date, sensor=None):

    assert(sensor == None or sensor_id == sensor.id)

    csv_filename = buildCSVurl(sensor_id, sensor_type, date)
    content = getCSVContent(csv_filename)

    cr = csv.reader(content.splitlines(), delimiter=';')
    my_list = list(cr)
    if not firstLineValid(my_list[0]):
        print("error in this file - format not correct")
        return False

    first_sensor = my_list[1]

    if sensor == None:
        sensor = Sensor(first_sensor[0], first_sensor[1], first_sensor[2],first_sensor[3], first_sensor[4])
    for row in my_list[1:]:
        assert(row[0] == first_sensor[0] and row[1] == first_sensor[1] and row[2] == first_sensor[2] and row[3] == first_sensor[3] and row[4] == first_sensor[4])
        new_datapoint = SensorData(row[5], row[6], row[7], row[8], row[9], row[10])
        sensor.addDatapoint(new_datapoint)
        print(row)

    return sensor


#---------------------------------------------------------------------------------
class SensorEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        return o.__dict__


def saveSensor(sensor_object : Sensor, day):


    with open(buildFilename(sensor_object.id, sensor_object.type, day) + ".json", 'w', encoding='utf-8') as file:
        json.dump(sensor_object, file, ensure_ascii=False, indent=2, cls=SensorEncoder)

# from_time and to_time are date_time objects
def getData(sensor_id, from_time, to_time):

    from_time_string = ""
    sensor_type = getSensorType(sensor_id)

    if isinstance(from_time, datetime.datetime):
        from_time_string = from_time.strftime("%Y-%m-%d")

    # todo: validation check time
    # todo check if in cache

    #  crawl data
    current_time = from_time
    requested_sensor = None
    while(current_time <= to_time):
        current_time_string = current_time.strftime("%Y-%m-%d")
        if current_time == from_time:
            requested_sensor = getDataOfOneDay(sensor_id, sensor_type, current_time_string)
        else:
            requested_sensor = getDataOfOneDay(sensor_id, sensor_type, current_time_string, requested_sensor)

        current_time += timedelta(days=1)


    # todo push into cache system

    saveSensor(requested_sensor, from_time_string)
    return requested_sensor


def main():


    # example call
    from_time = datetime.datetime(2021, 2, 1)
    to_time = datetime.datetime(2021,2,2)


    sensor = getData(141, from_time, to_time);
    pass

if __name__ == "__main__":
    main()

