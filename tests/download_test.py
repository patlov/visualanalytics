import unittest
import clustering as c
import api as a
import os
import datetime

class TestDownload(unittest.TestCase):
    def test_graz_sensors(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 3, 3)
        sensors = a.get_sensors("AUT", "Steiermark", "Graz", return_sensorids=True)
        sensor_list = a.download_sensors(sensors, from_time, to_time)
        self.assertEqual(len(sensor_list), 77)

    def test_graz_sensors_larger_duration(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 5, 1)
        sensors = a.get_sensors("AUT", "Steiermark", "Graz", return_sensorids=True)
        sensor_list = a.download_sensors(sensors, from_time, to_time)
        self.assertEqual(len(sensor_list), 85)

    def test_styria_sensors(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 3, 3)
        sensors = a.get_sensors("AUT", "Steiermark", return_sensorids=True)
        sensor_list = a.download_sensors(sensors, from_time, to_time)
        self.assertEqual(len(sensor_list), 159)

    def test_austria_sensors(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 3, 3)
        sensors = a.get_sensors("AUT", return_sensorids=True)
        sensor_list = a.download_sensors(sensors, from_time, to_time)
        self.assertEqual(len(sensor_list), 642)

if __name__ == '__main__':
    unittest.main()
