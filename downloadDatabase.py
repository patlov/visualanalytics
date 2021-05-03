
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json

local_path = "database/"
base_url = "http://archive.sensor.community/"
ext = "csv"

sensors_path = "database/sensors.json"

def writeSensorToJson(sensor_id, sensor_type):
    with open(sensors_path, "r") as jsonFile:
        data = json.load(jsonFile)

    if sensor_id in data:
        return

    data[sensor_id] = sensor_type
    with open(sensors_path, "w", encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile ,ensure_ascii=False, indent=2)


def geURLContent(url):
    return requests.get(url).text

def getCSVFileNamesInFolder(url, extension):
    content = geURLContent(url)
    soup = BeautifulSoup(content, 'html.parser')
    return [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(extension)]

def fileExists(folder_name, filename):
    if Path(local_path + folder_name + filename).is_file():
        print(folder_name + filename + " already exists")
        return True
    else:
        print(folder_name + filename + " creating")
        return False

def downloadSensorIdAndType(folder_url):

    csv_list = getCSVFileNamesInFolder(folder_url, ext)
    if not csv_list: # empty list
        print(folder_url + " not exists on server")

    for csv_url in csv_list:
        filename = csv_url[42:]

        list_of_underlines = [i for i in range(len(filename)) if filename.startswith('_', i)]
        sensor_type = filename[list_of_underlines[0] + 1: list_of_underlines[1]]
        sensor_id = filename[list_of_underlines[2] + 1: len(filename) - 4]

        writeSensorToJson(sensor_id, sensor_type)


def downloadFolder(folder_url):

    csv_list = getCSVFileNamesInFolder(folder_url, ext)
    if not csv_list: # empty list
        print(folder_url + " not exists on server")

    for csv_url in csv_list:
        print(csv_url)
        req = requests.get(csv_url)
        url_content = req.content
        folder_name = csv_url[32:42]
        filename = csv_url[42:]

        if fileExists(folder_name, filename): # only download files we did not downloaded yet
            continue

        try:
            file = open(local_path + folder_name + filename, 'wb')
        except FileNotFoundError: # create folder if it does not exist
            Path(local_path + folder_name).mkdir(parents=True, exist_ok=True)
            file = open(local_path + csv_url[32:], 'wb')

        file.write(url_content)
        file.close()

def download():

    year_range_from = 2021
    year_range_to = 2022 # excluding

    month_range_from = 1
    month_range_to = 2 # excluding

    day_range_from = 1
    day_range_to = 2 # excluding

    for year in range(year_range_from,year_range_to):
        for month in range(month_range_from,month_range_to):
            for day in range(day_range_from,day_range_to):

                if month < 10:
                    month_str = '0' + str(month)
                else:
                    month_str = str(month)

                if day < 10:
                    day_str = '0' + str(day)
                else:
                    day_str = str(day)

                date = str(year) + '-' + month_str + '-' + day_str
                # downloadFolder(base_url + date + '/')
                # downloadSensorIdAndType(base_url + date + '/')



def main():
    download()


if __name__ == "__main__":
    main()