import unittest
import api as a

class TestGeo(unittest.TestCase):
    def test_no_geo(self):
        sensors = a.get_sensors()
        self.assertEqual(len(sensors), 80)

    def test_all_geo(self):
        sensors = a.get_sensors(return_sensors=True)
        self.assertEqual(len(sensors), 27631)

    def test_all_contry_geo(self):
        sensors = a.get_sensors("AUT", return_sensors=True)
        self.assertEqual(len(sensors), 724)

    def test_all_state_geo(self):
        sensors = a.get_sensors("AUT", "Steiermark", return_sensors=True)
        self.assertEqual(len(sensors), 172)

    def test_all_city_geo(self):
        sensors = a.get_sensors("AUT", "Steiermark", "Graz", return_sensors=True)
        self.assertEqual(len(sensors), 89)

    def test_one_geo(self):
        sensors = a.get_sensors("AUT")
        self.assertEqual(len(sensors), 9)

    def test_two_geo(self):
        sensors = a.get_sensors("AUT", "Steiermark")
        self.assertEqual(len(sensors), 39)

    def test_three_geo(self):
        sensors = a.get_sensors("AUT", "Steiermark", "Graz")
        self.assertEqual(len(sensors), 89)

    def test_wrong_county(self):
        sensors = a.get_sensors("LALALAND")
        self.assertEqual(len(sensors), 80)

    def test_wrong_state(self):
        sensors = a.get_sensors("AUT", "LALALAND")
        self.assertEqual(len(sensors), 9)

    def test_wrong_city(self):
        sensors = a.get_sensors("AUT", "Steiermark", "LALALAND")
        self.assertEqual(len(sensors), 39)


if __name__ == '__main__':
    unittest.main()
