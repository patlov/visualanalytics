import json
import requests
import numpy as np
import pandas as pd


def get_key():
    with open('keys/here_key') as f:
        return f.read()


def download(url):
    r = requests.get(url)
    return r.content.decode(r.encoding)


def append_to_dataframe(df):
    lats = df['lat']
    lons = df['lon']

    countries = []
    states = []
    cities = []

    for i in range(len(lats)):
        country, state, city = get_country_info(lats[i], lons[i])
        countries.append(country)
        states.append(state)
        cities.append(city)

    df['country'] = countries
    df['state'] = states
    df['city'] = cities

    return df


def get_country_info(lat, lon):
    key = get_key()
    base_url = f"https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?prox={lat},{lon},250&mode=retrieveAddresses&maxresults=1&gen=9&apiKey={key}"
    data = download(base_url)
    data_json = json.loads(data)['Response']

    adress = data_json['View'][0]['Result'][0]['Location']['Address']

    country = adress['Country']

    state = None

    if 'State' in adress:
        state = adress['State']
    elif 'County' in adress:
        state = adress['County']

    city = adress['City']

    return country, state, city


def main():
    print(get_country_info(43, 11))


if __name__ == "__main__":
    main()
