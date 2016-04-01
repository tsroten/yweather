try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
import os
import unittest
import xml.etree.ElementTree

import yweather


class testFetchXml(unittest.TestCase):

    def setUp(self):
        self.client = yweather.Client()
        data_file_name = os.path.join(os.path.dirname(__file__),
                                      "data", "data_woeid.xml")
        with open(data_file_name) as f:
            root = xml.etree.ElementTree.parse(f).getroot()
        self.woeid = root.find("results/Result/woeid").text

    def test_fetch_xml(self):
        url = yweather.WOEID_LOOKUP_URL.format(quote("Raleigh, NC"))
        root = self.client._fetch_xml(url)
        self.assertEqual(root.find("results/Result/woeid").text, self.woeid)


class testFetchWoeid(unittest.TestCase):

    def return_root(self, extra=None):
        return self.root

    def setUp(self):
        self.client = yweather.Client()
        data_file_name = os.path.join(os.path.dirname(__file__),
                                      "data", "data_woeid.xml")
        with open(data_file_name) as f:
            self.root = xml.etree.ElementTree.parse(f).getroot()
        self.client._fetch_xml = self.return_root

    def test_fetch_woeid(self):
        self.assertEqual(self.client.fetch_woeid("Raleigh, NC"), "2478307")


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


class testFetchWeatherLidMode(unittest.TestCase):

    def return_root(self, extra=None):
        return self.root

    def setUp(self):
        self.client = yweather.Client()
        data_file_name = os.path.join(os.path.dirname(__file__),
                                      "data", "data_5day.xml")
        with open(data_file_name) as f:
            self.root = xml.etree.ElementTree.parse(f).getroot()
        self.client._fetch_xml = self.return_root

    def test_fetch_weather_lid_mode(self):
        weather = self.client.fetch_weather("USNC0558")
        self.assertEqual(weather["ttl"], "60")
        self.assertEqual(len(weather["forecast"]), 5)


class testFetchLid(unittest.TestCase):

    def return_root(self, extra=None):
        return self.root

    def setUp(self):
        self.client = yweather.Client()
        data_file_name = os.path.join(os.path.dirname(__file__),
                                      "data", "data_weather.xml")
        with open(data_file_name) as f:
            self.root = xml.etree.ElementTree.parse(f).getroot()
        self.client._fetch_xml = self.return_root

    def test_fetch_lid(self):
        self.assertEqual(self.client.fetch_lid("2478307"), "USNC0558")
