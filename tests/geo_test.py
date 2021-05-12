import unittest
import api as a

class TestGeo(unittest.TestCase):
    def test_no_geo(self):
        sensors = a.get_geo_info()
        self.assertEqual(len(sensors), 80)

    def test_one_geo(self):
        sensors = a.get_geo_info("AUT")
        self.assertEqual(len(sensors), 9)

    def test_two_geo(self):
        sensors = a.get_geo_info("AUT", "Steiermark")
        self.assertEqual(len(sensors), 39)

    def test_three_geo(self):
        sensors = a.get_geo_info("AUT", "Steiermark", "Graz")
        self.assertEqual(len(sensors), 89)

    def test_wrong_county(self):
        sensors = a.get_geo_info("LALALAND")
        self.assertEqual(len(sensors), 80)

    def test_wrong_state(self):
        sensors = a.get_geo_info("AUT", "LALALAND")
        self.assertEqual(len(sensors), 9)

    def test_wrong_city(self):
        sensors = a.get_geo_info("AUT", "Steiermark", "LALALAND")
        self.assertEqual(len(sensors), 39)


if __name__ == '__main__':
    unittest.main()