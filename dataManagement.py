import os
import pandas as pd
import numpy as np
from downloadDatabase import getCSVFileNamesInFolder
import json
import here as h
import sys
from datetime import datetime


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def findCountry(country_dict,sensors_dict_export, sensor, sensor_type):

    array = sensor.split('_')
    if isInt(array[0]):
        sensor = int(array[0])
    elif len(array) == 2:
        if isInt(array[0]):
            sensor = int(array[0])
        elif isInt(array[1]):
            sensor = int(array[1])
    elif len(array) == 3:
        if isInt(array[0]):
            sensor = int(array[0])
        elif isInt(array[1]):
            sensor = int(array[1])
        elif isInt(array[2]):
            sensor = int(array[2])
    else:
        print("sensor not valid: ", sensor)
        return

    for country in country_dict:
        for state in country_dict[country]:
            for city in country_dict[country][state]:
                sensor_list = country_dict[country][state][city]
                if sensor in sensor_list:
                    sensors_dict_export[sensor] = [sensor_type, country, state, city]
                    return

    print("sensor not found: ", str(sensor))


def findSensorTypeInSensorDict(sensor):
    sensor = str(sensor)
    sensors_dict = getSensorsJson()
    for sensor_id in sensors_dict:
        if sensor == sensor_id:
            sensor_type = sensors_dict[sensor_id][0]
            print("---> sensor found in dict")
            printToLog(sensor_id, "-> sensor found in dict")
            return sensor_type

    return "undefined"

def findSensorTypeInCSV(sensor):
    sensor = str(sensor)
    csv_files = getCSVFiles()

    for f in csv_files:

        filename = f[42:]
        list_of_underlines = [i for i in range(len(filename)) if filename.startswith('_', i)]
        sensor_type = filename[list_of_underlines[0] + 1: list_of_underlines[1]]
        sensor_id = filename[list_of_underlines[2] + 1: len(filename) - 4]
        if sensor == sensor_id:
            print("---> sensor found in file: ", f)
            printToLog(sensor_id, "-> sensor found in file " + filename)
            return sensor_type

    print("[ERROR] sensor id ", sensor, "not found in CSV")
    printToLog(sensor, "-> sensor not in DICT and NOT in FILE")
    return "undefined"


def iterateOverCountries():
    country_dict = getCountriesJson()

    for country in country_dict:
        for state in country_dict[country]:
            for city in country_dict[country][state]:
                sensor_list = country_dict[country][state][city]
                for i in range(len(sensor_list)):
                    sensor_list[i] = str(sensor_list[i])

    exportCountriesJson(country_dict)

def addCountriesToSensorList():
    country_dict = getCountriesJson()

    sensors_dict_export = {}

    for country in country_dict:
        for state in country_dict[country]:
            for city in country_dict[country][state]:
                sensor_list = country_dict[country][state][city]
                for sensor in sensor_list:
                    print("Search Sensor", sensor)
                    sensor_type = findSensorTypeInSensorDict(sensor)
                    if sensor_type == "undefined":
                        sensor_type = findSensorTypeInCSV(sensor)
                    sensors_dict_export[sensor] = [sensor_type, country, state, city]


    exportSensorsDict(sensors_dict_export)
    pass

def getCountryOfSensor(sensor_id):
    if isInt(sensor_id):
        sensor_id = str(sensor_id)
    sensors = getSensorsJson()
    if sensor_id not in sensors.keys():
        return None,None,None
    country = sensors[sensor_id][1]
    state = sensors[sensor_id][2]
    city = sensors[sensor_id][3]
    return country, state, city

def getCSVFiles():
    with open('database/csv_files.json', "r") as jsonFile:
        data = json.load(jsonFile)
    return data


def exportSensorsDict(sensors_dict):
    with open('database/sensors.json', "w", encoding='utf-8') as jsonFile:
        json.dump(sensors_dict, jsonFile, ensure_ascii=False, indent=2)

def getSensorsJson():
    with open('database/sensors.json', "r") as jsonFile:
        data = json.load(jsonFile)
    return data


def getCountriesJson():
    with open('database/country_sensors.json', "r") as jsonFile:
        data = json.load(jsonFile)
    return data

def exportCountriesJson(countries_dict):

    with open('database/country_sensors.json', "w", encoding='utf-8') as jsonFile:
        json.dump(countries_dict, jsonFile, ensure_ascii=False, indent=2)

#---------------------------------------------------------------------------------------------------------
def printToErrorLog(sensor_id, reason = None):
    error_file = open("database/error_log.txt", "a")
    now = datetime.now()
    error_file.write(now.strftime("%H:%M:%S") + "  " + str(sensor_id) + " : maybe a issue with lon lat\n")

def printToLog(sensor_id, reason = None):
    error_file = open("database/sensor_log.txt", "a")
    now = datetime.now()
    error_file.write(now.strftime("%H:%M:%S") + "  " + str(sensor_id) + reason + "\n")

def crawlCountriesToJson():
    folder_url = 'http://archive.sensor.community/2021-05-10/'
    # csv_files = getCSVFileNamesInFolder(folder_url, ext)
    csv_files = getCSVFiles()
    geo_cluster = {}

    current_sensor = 0

    for f in csv_files:
        try:
            df = pd.read_csv(f, sep=';')
            current_sensor = int(df['sensor_id'][0])
            print("opening file: ", f)
            lat = df['lat'][0]
            lon = df['lon'][0]
            if lat == 0 or lon == 0:
                country = 'undefined'
                if country not in geo_cluster:
                    geo_cluster[country] = []
                geo_cluster[country].append(int(df['sensor_id'][0]))
            else:
                country, state, city = h.get_country_info(lat, lon)
                if country not in geo_cluster:
                    geo_cluster[country] = {}

                if state not in geo_cluster[country]:
                    geo_cluster[country][state] = {}

                if city not in geo_cluster[country][state]:
                    geo_cluster[country][state][city] = []
                geo_cluster[country][state][city].append(int(df['sensor_id'][0]))
        except:
            printToErrorLog(sensor_id=current_sensor)

    exportCountriesJson(geo_cluster)


def main():

    # crawlCountriesToJson()
    #
    iterateOverCountries()
    pass

if __name__ == "__main__":
    main()
