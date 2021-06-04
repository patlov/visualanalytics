import database
import dataManagement
import itertools
import pandas as pd
from datetime import *
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

    step_size_minutes = database.calculateStepSize(from_time, to_time)

    for sensor_id in d.keys():
        dfs = d[sensor_id]
        ts = [(datetime.strptime(dfs[i].timestamp[0], '%Y-%m-%dT%H:%M:%S'), i) for i in range(len(dfs))]
        ts = sorted(ts, key=lambda tup: tup[0])
        dfs = [dfs[t[1]] for t in ts]

        df = pd.concat(dfs, ignore_index=True)
        lat, lon, sensor_type = df.lat[0], df.lon[0], df.sensor_type[0]

        df = df.dropna(axis=1, how='all')
        df.timestamp = pd.to_datetime(df.timestamp)
        df = df.set_index('timestamp')
        old_df = df.copy()
        df = df.resample(f"{step_size_minutes}min").ffill()
        df = df.drop(['sensor_id', 'sensor_type', 'lat', 'lon', 'location'], axis=1)

        # import matplotlib.pyplot as plt
        # plt.plot(old_df.index, old_df.temperature, label='original')
        # plt.plot(df.index, df.temperature, label=f'resample pandas {step_size_minutes} min.')
        # plt.legend()
        # plt.grid()
        # plt.show()

        country, state, city = dataManagement.getCountryOfSensor(sensor_id)
        if country == None:
            country, state, city = h.get_country_info(lat, lon)
        s = Sensor(sensor_id, sensor_type, country, state, city, lat, lon, df)
        sensors.append(s)

    return sensors

def get_geo_info(country=None, state=None, city=None, return_cities=False):
    countries_dict = dataManagement.getCountriesJson()
    elems = [country, state, city]
    result = safe_get(countries_dict, elems, return_cities)

    return result