import unittest
import clustering as c
import api as a
import os
import datetime

class TestCluster(unittest.TestCase):
    def test_basic_cluster(self):
        sensors = a.get_geo_info("AUT", "Steiermark", "Graz")
        pass

    def test_get_many_sensors(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 4, 3)
        os.chdir('../')
        sensors = a.get_geo_info("DEU", "Bayern", "Dachau")
        sensor_list = []
        for sensor_id in sensors:
            sensor = a.getSensorData(sensor_id, from_time, to_time)
            if not sensor == None:
                sensor_list.append(sensor)

        pass

if __name__ == '__main__':
    unittest.main()
