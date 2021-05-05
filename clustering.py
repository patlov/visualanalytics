import os
import pandas as pd
import numpy as np


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
