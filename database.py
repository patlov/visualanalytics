import copy

import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import *
import csv
import json
import here as h
from classes import *
import gzip
import os

import dataManagement

local_path = "database/"
base_url = "http://archive.sensor.community/"
ext = "csv"
sensors_path = "database/sensors.json"
country_path = "database/country_sensors.json"

# if true, we save the json files in zipped mode, if false its in plaintext json
ZIP_MODE = False

def getSensorType(sensor_id):
    if isinstance(sensor_id, int):
        sensor_id = str(sensor_id)
    with open(sensors_path, "r") as jsonFile:
        data = json.load(jsonFile)

    if sensor_id not in data:
        print("error, sensor " + str(sensor_id) + " is not in list")
        return
    return data[sensor_id][0]


def getCSVContent(file_url):
    print(file_url)
    req = requests.get(file_url)
    content = req.content.decode('utf-8')
    return content


def buildCSVurl(sensor_id, sensor_type, day):
    return base_url + day + "/" + buildFilename(sensor_id, sensor_type, day) + ".csv"

def buildLocalPath(sensor_id, sensor_type, day):
    return local_path + day + "/" + buildFilename(sensor_id, sensor_type, day) + ".json"

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
    # ??????
    # assert(sensor == None or sensor_id == sensor.id)

    csv_filename = buildCSVurl(sensor_id, sensor_type, date)
    content = getCSVContent(csv_filename)

    cr = csv.reader(content.splitlines(), delimiter=';')
    my_list = list(cr)
    assert(firstLineValid(my_list[0]))

    first_sensor = my_list[1]

    if sensor == None:
        country, state, city = dataManagement.getCountryOfSensor(sensor_id)
        if country == None:
            country, state, city = h.get_country_info(first_sensor[3], first_sensor[4])
        sensor = Sensor(first_sensor[0], first_sensor[1], country, state, city,first_sensor[3], first_sensor[4])

    for row in my_list[1:]:
        assert(row[0] == first_sensor[0] and row[1] == first_sensor[1] and row[2] == first_sensor[2] and row[3] == first_sensor[3] and row[4] == first_sensor[4])
        sensor.addDatapoint(row[5], row[6], row[7], row[8], row[9], row[10])
        print(row)

    return sensor


#---------------------------------------------------------------------------------
class SensorEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

        return o.__dict__


def calculateStepSize(from_time : datetime.datetime, to_time : datetime.datetime):
    assert(from_time < to_time)
    timedelta = to_time - from_time
    minutes = int(timedelta.total_seconds() / 60)
    step_size = int(minutes / 100)
    return step_size


def saveSensor(sensor_object : Sensor, day):

    sensor_copy = copy.copy(sensor_object)
    global ZIP_MODE

    if not os.path.exists(local_path + day): # if folder nox exists, create it
        Path(local_path + day).mkdir(parents=True, exist_ok=True)

    filename = buildLocalPath(sensor_copy.id, sensor_copy.type, day)
    if os.path.exists(filename):
        return

    df = sensor_copy.dataFrame.to_json(orient="records")
    sensor_copy.dataFrame = json.loads(df)
    if ZIP_MODE:
        with gzip.open(filename, 'wt', encoding='utf-8') as file:
            json.dump(sensor_copy, file, ensure_ascii=False, indent=2, cls=SensorEncoder)
    else:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(sensor_copy, file, ensure_ascii=False, indent=2, cls=SensorEncoder)

def reduceDatatoStepSize(sensor : Sensor, step_size_minutes : int):
    sensor_data = sensor.dataFrame
    time_of_last = sensor_data.iloc[0]['timestamp']

    time_of_last = datetime.datetime.strptime(time_of_last, '%Y-%m-%dT%H:%M:%S')

    for i,row in sensor_data.iterrows():
        time_of_current = row['timestamp']
        time_of_current = datetime.datetime.strptime(time_of_current, '%Y-%m-%dT%H:%M:%S')
        if time_of_current == time_of_last:
            continue
        time_of_next = time_of_last + datetime.timedelta(hours=0, minutes=step_size_minutes, seconds=0)

        if time_of_current < time_of_next:
            sensor_data.drop(i, inplace=True)
        else:
            time_of_last = time_of_current

    assert len(sensor_data.index) <= 100 # or David has done the calculation wrong (again)
    pass

# from_time and to_time are date_time objects
def getData(sensor_id, from_time, to_time):

    from_time_string = ""
    sensor_type = getSensorType(sensor_id)

    if isinstance(from_time, datetime.datetime):
        from_time_string = from_time.strftime("%Y-%m-%d")

    # todo: validation check time
    if from_time == to_time:
        to_time += timedelta(days=1)
    # todo check if in cache

    #  crawl data
    current_time = from_time
    requested_sensor = None
    while(current_time < to_time):
        current_time_string = current_time.strftime("%Y-%m-%d")
        if current_time == from_time:
            requested_sensor = getDataOfOneDay(sensor_id, sensor_type, current_time_string)
        else:
            requested_sensor = getDataOfOneDay(sensor_id, sensor_type, current_time_string, requested_sensor)

        current_time += timedelta(days=1)


    # todo push into cache system

    saveSensor(requested_sensor, from_time_string)


    step_size_minutes = calculateStepSize(from_time, to_time)
    reduceDatatoStepSize(requested_sensor, step_size_minutes)

    return requested_sensor


def main():


    # example call
    from_time = datetime.datetime(2021, 2, 1)
    to_time = datetime.datetime(2021,2,2)

    sensor = getData(141, from_time, to_time)
    pass

if __name__ == "__main__":
    main()

