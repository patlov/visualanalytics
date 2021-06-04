import database
import dataManagement
import itertools
import pandas as pd
from multiprocessing import Pool
from classes import Sensor
from utils import get_sensor_urls, unnest_dicts, safe_get, download_wrapper

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

    sensors = []

    for sensor_id in d.keys():
        dfs = d[sensor_id]
        df = pd.concat(dfs, ignore_index=True)
        df = df.dropna(axis=1, how='all')
        dropped_df = df.drop(['sensor_id', 'sensor_type', 'lat', 'lon', 'location'], axis=1)
        country, state, city = dataManagement.getCountryOfSensor(sensor_id)
        lat = df.lat[0]
        lon = df.lon[0]
        if country == None:
            country, state, city = h.get_country_info(lat, lon)
        sensors.append(Sensor(sensor_id, df.sensor_type[0], country, state, city, lat, lon, dropped_df))

    return sensors

def get_geo_info(country=None, state=None, city=None, return_cities=False):
    countries_dict = dataManagement.getCountriesJson()
    elems = [country, state, city]
    result = safe_get(countries_dict, elems, return_cities)

    return result