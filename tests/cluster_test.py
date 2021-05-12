import unittest
import clustering as c
import api as a


class TestCluster(unittest.TestCase):
    def test_basic_cluster(self):
        sensors = a.get_geo_info("AUT", "Steiermark", "Graz")
        pass


if __name__ == '__main__':
    unittest.main()
