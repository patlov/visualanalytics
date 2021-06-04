import pandas as pd
from datetime import *

def cleanup_dataframe(dfs, resampling_time):
    # Sort dataframes by timestamp
    ts = [(datetime.strptime(dfs[i].timestamp[0], '%Y-%m-%dT%H:%M:%S'), i) for i in range(len(dfs))]
    ts = sorted(ts, key=lambda tup: tup[0])
    dfs = [dfs[t[1]] for t in ts]

    # Cat dataframes together
    df = pd.concat(dfs, ignore_index=True)
    lat, lon, sensor_type = df.lat[0], df.lon[0], df.sensor_type[0]

    # Drop NaN values
    df = df.dropna(axis=1, how='all')

    # Set timestamp as index
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp')
    df = df[~df.index.duplicated(keep='first')]

    # Resample dataframe
    df = df.resample(f"{resampling_time}min").ffill()
    df = df.drop(['sensor_id', 'sensor_type', 'lat', 'lon', 'location'], axis=1)
    df = df.replace(r'[a-z]+$', 'nan', regex=True)
    df = df.astype("float")
    df = df.interpolate(method='linear', limit_direction='both')

    # plt.show()

    return sensor_type, lat, lon, df

def align_sensors(sensors):
    pass

