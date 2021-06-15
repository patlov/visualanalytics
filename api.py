import database
import dataManagement
import itertools
import pandas as pd
from datetime import *
from multiprocessing import Pool
from classes import Sensor
from utils import get_sensor_urls, unnest_dicts, safe_get, download_wrapper
from preprocess import cleanup_dataframe

def download_sensors(sensor_ids, from_time, to_time):
    file_names = []
    sensor_ids_names = []
    for i in sensor_ids:
        file_names.append(get_sensor_urls(i, from_time, to_time))
        sensor_ids_names.append([i] * len(file_names[-1]))

    sensor_ids_names = list(itertools.chain(*sensor_ids_names))
    file_names= list(itertools.chain(*file_names))

    zipped_params = list(zip(sensor_ids_names, file_names))
    pool = Pool()
    result = pool.map(download_wrapper, zipped_params)
    d = {}

    for e in result:
        k = e[0]
        v = e[1]

        if v is None:
            continue

        if not k in d:
            d[k] = []

        d[k].append(v)

    sensors = {}

    step_size_minutes = database.calculateStepSize(from_time, to_time)

    for sensor_id in d.keys():
        dfs = d[sensor_id]
        sensor_type, lat, lon, df = cleanup_dataframe(dfs, step_size_minutes)
        country, state, city = dataManagement.getCountryOfSensor(sensor_id)

        if country == None:
            country, state, city = h.get_country_info(lat, lon)
        s = Sensor(sensor_id, sensor_type, country, state, city, lat, lon, df)
        sensors[sensor_id] = s

    return sensors

def get_state_sensors(countries=None, type=None, num_cities=1):
    countries_dict = dataManagement.getCountriesJson()
    sensors = []

    if not countries:
        countries = list(countries_dict.keys())

    for k in countries:
        sensors.extend(get_sensors(k, return_sensors=True, num_sensors=num_cities, type=type))

    return sensors

def unfold_types(countries_dict, type):
    for c in countries_dict:
        for s in countries_dict[c]:
            for ct in countries_dict[c][s]:
                types = countries_dict[c][s][ct]
                types_to_parse = list(types)
                if type:
                    types_to_parse = type
                res = []
                for t in types_to_parse:
                    if t in types:
                        res.extend(types[t])
                countries_dict[c][s][ct] = res
    return countries_dict

def get_sensors(country=None, state=None, city=None, type=None, return_sensors=False, sensor_per_city=None, num_sensors=None):
    countries_dict = dataManagement.getCountriesJson()
    countries_dict = unfold_types(countries_dict, type)
    elems = [country, state, city]
    result = safe_get(countries_dict, elems, return_sensors, sensor_per_city, num_sensors)

    return result