import os
import unittest
import xml.etree.ElementTree

import yweather

class testYWeather(unittest.TestCase):

    def setUp(self):
        self.client = yweather.Client()

    def test_fetch_woeid(self):
        self.assertEqual(self.client.fetch_woeid("23454"), "12767391")
        self.assertEqual(self.client.fetch_woeid("kajlsfj"), None)

class testFetchWeather(unittest.TestCase):

    def return_root(self, extra=None):
        return self.root

    def setUp(self):
        self.client = yweather.Client()
        data_file_name = os.path.join(os.path.dirname(__file__),
                                      "data", "data_weather.xml")
        with open(data_file_name) as f:
            self.root = xml.etree.ElementTree.parse(f).getroot()
        self.client._fetch_xml = self.return_root

    def test_fetch_weather(self):
        weather = self.client.fetch_weather("2478307")
        self.assertEqual(weather["ttl"], "60")
        self.assertEqual(weather["wind"]["direction"], "240")
        self.assertEqual(weather["forecast"][0]["high"], "52")
        self.assertEqual(weather["geo"]["lat"], "35.79")
        
