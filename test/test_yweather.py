import unittest

import yweather

class testYWeather(unittest.TestCase):

    def setUp(self):
        self.client = yweather.Client()

    def test_fetch_woeid(self):
        self.assertEqual(self.client.fetch_woeid("23454"), "12767391")
        self.assertEqual(self.client.fetch_woeid("kajlsfj"), None)
