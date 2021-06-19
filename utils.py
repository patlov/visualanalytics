import itertools
import pandas as pd
from io import StringIO
from datetime import *
import os
from random import sample

import database
import dataManagement

def unnest_dicts(d, max_vals):
    for v in d.values():
        if isinstance(v, dict):
            yield from unnest_dicts(v, max_vals)
        else:
            if max_vals and max_vals < len(v):
                yield v[:max_vals]
            else:
                yield v

def sample_dicts(d, num_elems):
    if isinstance(d, dict):
        n_key = sample(list(d.keys()), 1)[0]
        yield from sample_dicts(d[n_key], num_elems)
    else:
        yield sample(d, min(len(d), num_elems))

def safe_get(dc, elems, return_cities=False, sensor_per_city=None, num_cities=None):
    tmp_dc = dc
    for e in elems:
        if e and e in tmp_dc:
            tmp_dc = tmp_dc[e]
        else:
            break

    if isinstance(tmp_dc, dict):
        if not return_cities:
            tmp_dc = list(tmp_dc.keys())
        else:
            if not num_cities:
                tmp_dc = list(unnest_dicts(tmp_dc, sensor_per_city))
                tmp_dc = list(itertools.chain(*tmp_dc))
            else:
                results = []
                for k in tmp_dc.keys():
                    results.extend(list(sample_dicts(tmp_dc[k], num_cities)))

                return [sl for l in results for sl in l]
    elif num_cities:
        tmp_dc = sample(tmp_dc, num_cities)

    return tmp_dc

def download_wrapper(zipped):
    return get_sensor_one_day(zipped[0], zipped[1])

def get_cache(csv_filename):
    split = csv_filename.split('/')
    date = split[3]
    file_name = split[4]

    folder = f"database/cache/{date}"
    path = folder + '/' + file_name
    content = None

    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
        print(f"Reading from cache: {csv_filename}")

    return content

def write_cache(csv_filename, content):
    split = csv_filename.split('/')
    date = split[3]
    file_name = split[4]

    folder = f"database/cache/{date}"
    if not os.path.isdir(folder):
        os.mkdir(folder)

    path = folder + '/' + file_name

    with open(path, 'w') as f:
        f.write(content)

    return content

def get_sensor_one_day(sensor_id, csv_filename):
    content = get_cache(csv_filename)
    try:
        if content == "INVALID":
            raise FileNotFoundError("Url " + csv_filename + "  not exists")
        if not content:
            content = database.getCSVContent(csv_filename)
            write_cache(csv_filename, content)
    except Exception as e:
        write_cache(csv_filename, "INVALID")
        dataManagement.printToErrorLog(sensor_id, str(e))
        return sensor_id, None

    df = pd.read_csv(StringIO(content), sep=';')
    return sensor_id, df

def calcDownloadStepSize(from_time, to_time):
    import numpy as np
    diff = to_time - from_time
    return max(round(diff.days * 0.1), 1)

def get_sensor_urls(sensor_id, from_time, to_time, delta=None):
    if not delta:
        delta = calcDownloadStepSize(from_time, to_time)

    sensor_type = database.getSensorType(sensor_id)

    current_time = from_time
    file_names = []
    while(current_time < to_time):
        current_date_string = current_time.strftime("%Y-%m-%d")
        csv_filename = database.buildCSVurl(sensor_id, sensor_type, current_date_string)
        file_names.append(csv_filename)
        current_time += timedelta(days=delta)

    return file_names