import os
import pandas as pd
import numpy as np
from downloadDatabase import getCSVFileNamesInFolder
import json
import here as h
import sys
from datetime import datetime
from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series_dataset
import matplotlib.pyplot as plt
import warnings
from fastdtw import fastdtw
from collections import OrderedDict

import random as r
import numpy as np

r.seed(1)
np.random.seed(1)

def get_df_dict(sensors, vector, min_val, max_val):
    d_s = {}

    for k in sensors.keys():
        s = sensors[k]
        if vector in s.dataFrame:
            series = s.dataFrame[vector]
            if min_val < series.min() and max_val > series.max():
                d_s[s.id] = s.dataFrame[vector]

    return d_s

def cluster_ts(sensors, vector, n_clusters, min_val, max_val, max_iter=100):
    warnings.filterwarnings('ignore')
    d_s = get_df_dict(sensors, vector, min_val, max_val)
    dataset = to_time_series_dataset(list(d_s.values()))

    model = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw", max_iter=max_iter, n_jobs=-1)
    labels = model.fit_predict(dataset)
    s = model.cluster_centers_.shape

    result = {}
    sensor_ids = list(d_s.keys())

    for i in range(len(labels)):
        if not labels[i] in result:
            result[labels[i]] = {'centroid': model.cluster_centers_[labels[i]], 'sensor_ids': [], 'centroid_ds': [], "db_indices": []}
        result[labels[i]]['sensor_ids'].append(str(sensor_ids[i]))
        centroid = model.cluster_centers_[labels[i]]
        tmp_sensor = np.array(d_s[sensor_ids[i]])
        result[labels[i]]['centroid_ds'].append(fastdtw(centroid, tmp_sensor.reshape(tmp_sensor.shape[0],1))[0])

    for i in result.keys():
        vi = result[i]
        for j in result.keys():
            if i == j:
                continue
            vj = result[j]
            dij = fastdtw(vi['centroid'], vj['centroid'])[0]
            Rij = (np.mean(vi['centroid_ds']) + np.mean(vj['centroid_ds'])) / dij
            vi['db_indices'].append(Rij)

    end_result = []

    for k in result.keys():
        v = result[k]
        end_result.append((max(v['db_indices']), v))

    end_result = sorted(end_result, key=lambda tup: tup[0])

    return end_result

def cluster_countries(main_folder):
    csv_files = parse_folder(main_folder)

    geo_cluster = {}

    for f in csv_files:
        df = pd.read_csv(f)
        country, state, city = df['country'][0], df['state'][0], df['city'][0]
        if country not in geo_cluster:
            geo_cluster[country] = {}

        if state not in geo_cluster[country]:
            geo_cluster[country][state] = {}

        if city not in geo_cluster[country][state]:
            geo_cluster[country][state][city] = []

        geo_cluster[country][state][city].append(df)
    return geo_cluster


def parse_folder(main_folder):
    csv_files = []
    for path, subdirs, files in os.walk(main_folder):
        for name in files:
            if str(name).endswith('.csv'):
                csv_files.append(os.path.join(path, name))
    return csv_files


def main():
    cluster_countries('database')


if __name__ == "__main__":
    main()
