import copy
import datetime

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
ZIP_MODE = True

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
    if req.status_code == 404:
        raise FileNotFoundError("Url " + file_url + "  not exists")
    content = req.content.decode('utf-8')
    return content


def buildCSVurl(sensor_id, sensor_type, day):
    return base_url + day + "/" + buildFilename(sensor_id, sensor_type, day) + ".csv"

def buildLocalPath(sensor_id, sensor_type, day):
    return local_path + day + "/" + buildFilename(sensor_id, sensor_type, day) + ".json"

def buildFilename(sensor_id, sensor_type, day):
    return day + "_" + str(sensor_type) + "_sensor_" + str(sensor_id)


def checkFileFormat(header):
    if header[0] != 'sensor_id' or header[1] != 'sensor_type' or header[2] != 'location' \
            or header[3] != 'lat' or header[4] != 'lon' or header[5] != 'timestamp':
        raise NameError("File Format not valid - name error at id, type, loc, lat, lon or timestamp")

    if header[6] != 'pressure' or header[7] != 'altitude' or header[8] != 'pressure_sealevel' or \
        header[9] != 'temperature' or header[10] != 'humidity':
        raise NameError("File Format not valid - name error at pressure, lat, pres, temp, hum")

    return True


def getDataOfOneDay(sensor_id, sensor_type, date, sensor=None):

    csv_filename = buildCSVurl(sensor_id, sensor_type, date)

    try:
        content = getCSVContent(csv_filename)
        cr = csv.reader(content.splitlines(), delimiter=';')
        my_list = list(cr)
        checkFileFormat(my_list[0])

    except FileNotFoundError as e:
        dataManagement.printToErrorLog(sensor_id, str(e))
        return None, []
    except NameError as e:
        dataManagement.printToErrorLog(sensor_id, e)
        return None, []

    first_sensor = my_list[1]
    dataPoints = []

    if sensor == None:
        country, state, city = dataManagement.getCountryOfSensor(sensor_id)
        if country == None:
            country, state, city = h.get_country_info(first_sensor[3], first_sensor[4])
        sensor = Sensor(first_sensor[0], first_sensor[1], country, state, city,first_sensor[3], first_sensor[4])

    for row in my_list[1:]:
        if not (row[0] == first_sensor[0] and row[1] == first_sensor[1] and row[2] == first_sensor[2] and row[3] == first_sensor[3] and row[4] == first_sensor[4]):
            raise NameError("Entry " + str(row) + "  not in same format as first line: " + str(first_sensor))
        dataPoints.append({'timestamp':row[5], 'pressure':row[6], 'altitude':row[7], 'pressure_sealevel':row[8], 'temperature':row[9], 'humidity': row[10]})

    return sensor, dataPoints


#---------------------------------------------------------------------------------
class SensorEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

        return o.__dict__


def calculateStepSize(from_time : datetime.datetime, to_time : datetime.datetime):
    if from_time > to_time:
        raise ValueError("from_time must be smaller than to_time")
    timedelta = to_time - from_time
    minutes = int(timedelta.total_seconds() / 60)
    step_size = int(minutes / 100)
    return step_size


def saveSensor(sensor_object : Sensor, dataPoints : list,  day : datetime.datetime):

    day = day.strftime("%Y-%m-%d")
    # copy because we only want one day
    tmp_sensor = Sensor(sensor_object.id, sensor_object.type, sensor_object.country, sensor_object.state, sensor_object.city, sensor_object.lat, sensor_object.long)
    tmp_sensor.addDatapoints(dataPoints)

    global ZIP_MODE

    if not os.path.exists(local_path + day): # if folder nox exists, create it
        Path(local_path + day).mkdir(parents=True, exist_ok=True)

    filename = buildLocalPath(tmp_sensor.id, tmp_sensor.type, day)
    if os.path.exists(filename):
        return

    df = tmp_sensor.dataFrame.to_json(orient="records")
    tmp_sensor.dataFrame = json.loads(df)
    if ZIP_MODE:
        with gzip.open(filename, 'wt', encoding='utf-8') as file:
            json.dump(tmp_sensor, file, ensure_ascii=False, indent=2, cls=SensorEncoder)
    else:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(tmp_sensor, file, ensure_ascii=False, indent=2, cls=SensorEncoder)

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


    if len(sensor_data.index) > 100: # or David has done the calculation wrong (again)
        raise ValueError("Step size not correct calculated, not allowed to have more than 100 datapoints")
    pass

# from_time and to_time are date_time objects
def getData(sensor_id, from_time : datetime.datetime, to_time : datetime.datetime):

    sensor_type = getSensorType(sensor_id)

    if not isinstance(from_time, datetime.datetime) or not isinstance(to_time, datetime.datetime):
        raise TypeError("Time must be in datetime.datetime format")

    if from_time == to_time:
        to_time += timedelta(days=1)
    if from_time > to_time:
        raise ValueError("from_time must be smaller than to_time")
    # todo check if in cache

    #  crawl data
    current_time = from_time
    requested_sensor = None
    while(current_time < to_time):
        current_time_string = current_time.strftime("%Y-%m-%d")
        if current_time == from_time:
            requested_sensor, data_points = getDataOfOneDay(sensor_id, sensor_type, current_time_string)
        else:
            tmp_sensor, data_points = getDataOfOneDay(sensor_id, sensor_type, current_time_string, requested_sensor)
            if not tmp_sensor == None:
                requested_sensor = tmp_sensor
            if not requested_sensor == None and not len(data_points) == 0:
                requested_sensor.addDatapoints(data_points)
                # todo create thread for push into local database (cache)
                saveSensor(requested_sensor, data_points, current_time)


        current_time += timedelta(days=1)


    if requested_sensor == None:
        dataManagement.printToErrorLog(sensor_id, "sensor has no data in this time range")
        return None

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

