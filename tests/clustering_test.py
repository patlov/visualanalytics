import unittest
import clustering as c
import api as a
import os
import datetime
from clustering import cluster_ts
import matplotlib.pyplot as plt

class TestCluster(unittest.TestCase):
    def plot_cluster(self, cluster, sensor_list, vector):
        n_clusters = len(cluster)
        fig, axs = plt.subplots(n_clusters, sharex=True, sharey=True)

        for i in range(n_clusters):
            for j in range(len(cluster[i][1])):
                id = cluster[i][1][j]
                axs[i].plot(list(sensor_list[id].dataFrame[vector]), linewidth=1)
            axs[i].plot(cluster[i][0], linewidth=3)
            axs[i].grid()

        plt.show()

    def test_austria_sensors(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 3, 3)
        sensors = a.get_geo_info("AUT", "Steiermark", "Graz", return_cities=True)
        sensor_list = a.download_sensors(sensors, from_time, to_time)
        result = cluster_ts(sensor_list, 'temperature', 6, -50, 50)
        self.assertEqual(len(result), 6)
        # self.plot_cluster(result, sensor_list, 'temperature')

    def test_berlin_sensors(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 3, 3)
        sensors = a.get_geo_info("DEU", "Berlin", return_cities=True)
        sensor_list = a.download_sensors(sensors, from_time, to_time)
        result = cluster_ts(sensor_list, 'temperature', 6, -50, 50)
        self.assertEqual(len(result), 6)
        # self.plot_cluster(result, sensor_list, 'temperature')

    def test_world_sensors(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 3, 3)
        sensors = a.get_geo_info(return_cities=True, num_cities=1)
        sensor_list = a.download_sensors(sensors, from_time, to_time)
        result = cluster_ts(sensor_list, 'temperature', 6, -50, 50)
        self.assertEqual(len(sensors), 80)
        # self.plot_cluster(result, sensor_list, 'temperature')

    def test_germany_regional_sensors(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 3, 3)
        sensors = a.get_geo_info("DEU", return_cities=True, num_cities=1)
        sensor_list = a.download_sensors(sensors, from_time, to_time)
        result = cluster_ts(sensor_list, 'temperature', 4, -50, 50)
        self.assertEqual(len(sensors), 16)
        # self.plot_cluster(result, sensor_list, 'temperature')

    def test_all_states(self):
        from_time = datetime.datetime(2021, 3, 1)
        to_time = datetime.datetime(2021, 3, 3)
        sensors = a.get_state_sensors(num_cities=1, countries=["DEU", "AUT", "ITA"])
        sensor_list = a.download_sensors(sensors, from_time, to_time)
        result = cluster_ts(sensor_list, 'temperature', 4, -50, 50)
        self.assertEqual(len(sensors), 43)
        # self.plot_cluster(result, sensor_list, 'temperature')

if __name__ == '__main__':
    unittest.main()
