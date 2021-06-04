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

def get_df_dict(sensors, vector, min_val, max_val):
    d_s = {}

    for k in sensors.keys():
        s = sensors[k]
        if vector in s.dataFrame:
            series = s.dataFrame[vector]
            if min_val < series.min() and max_val > series.max():
                d_s[s.id] = s.dataFrame[vector]

    return d_s

def cluster_ts(sensors, vector, n_clusters, min_val, max_val, max_iter=20):
    d_s = get_df_dict(sensors, vector, min_val, max_val)
    dataset = to_time_series_dataset(list(d_s.values()))

    model = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw", max_iter=max_iter)
    labels = model.fit_predict(dataset)
    s = model.cluster_centers_.shape

    result = {}
    sensor_ids = list(d_s.keys())

    for i in range(len(labels)):
        if not labels[i] in result:
            result[labels[i]] = (model.cluster_centers_[labels[i]], [])
        result[labels[i]][1].append(str(sensor_ids[i]))

    return result

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
