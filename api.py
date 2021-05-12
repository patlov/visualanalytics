import database
import dataManagement
from datetime import *

def getSensorData(sensor_id : str, from_time : datetime, to_time : datetime):
    return database.getData(sensor_id, from_time, to_time)

def getSensorType(sensor_id : str):
    database.getSensorType(sensor_id)

def safe_get(dc, elems):
    tmp_dc = dc
    for e in elems:
        if e and e in tmp_dc:
            tmp_dc = tmp_dc[e]
        else:
            break

    return tmp_dc

def get_geo_info(country=None, state=None, city=None):
    countries_dict = dataManagement.getCountriesJson()
    result = safe_get(countries_dict, [country, state, city])

    if isinstance(result, dict):
        result = list(result.keys())

    return result