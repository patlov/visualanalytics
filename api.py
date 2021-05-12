
import database
import dataManagement
from datetime import *

def getSensorData(sensor_id : str, from_time : datetime, to_time : datetime):
    return database.getData(sensor_id, from_time, to_time)

def getSensorType(sensor_id : str):
    database.getSensorType(sensor_id)

def getCountries():
    countries_dict = dataManagement.getCountriesJson()
    return countries_dict.keys()

def getState(country : str):
    countries_dict = dataManagement.getCountriesJson()
    if country not in countries_dict:
        return None
    return countries_dict[country]

def getCity(country : str, state : str):
    countries_dict = dataManagement.getCountriesJson()
    if country not in countries_dict or state not in countries_dict:
        return None
    return countries_dict[country][state]

def getSensors(country : str, state : str, city : str):
    countries_dict = dataManagement.getCountriesJson()
    if country not in countries_dict or state not in countries_dict or city not in countries_dict:
        return None
    return countries_dict[country][state][city]