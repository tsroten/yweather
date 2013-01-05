# -*- coding: utf-8 -*-

#Copyright (c) 2012-2013 Thomas Roten

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnshished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""a Python module that provides an interface to the Yahoo! Weather RSS Feed.

Classes:
    Client: interface with the Yahoo! Weather RSS Feed.

Constants:
    WOEID_LOOKUP_URL: the URL used to fetch a location’s corresponding WOEID.
    WEATHER_URL: the URL used to fetch a WOEID's weather.
    LID_LOOKUP_URL: the URL used to fetch a location's corresponding LID.
    LID_WEATHER_URL: the URL used to fetch a LID's weather.
    WEATHER_NS: the XML namespace used in the weather RSS feed.
    GEO_NS: the XML namespace used for the lat/long coordinates in the RSS feed.
    CONDITION_IMAGE_URL: the URL of an image depicting the current conditions.
    UNITS: a dict that maps data names to units.

"""

try:
    from urllib.request import urlopen
    from urllib.parse import quote
except ImportError:
    from urllib2 import urlopen
    from urllib import quote
import contextlib
import re
import xml.etree.ElementTree


WOEID_LOOKUP_URL = ("http://locdrop.query.yahoo.com/v1/public/yql?"
                    "q=select%20woeid%20from%20locdrop.placefinder%20"
                    "where%20text='{0}'")
WEATHER_URL = "http://weather.yahooapis.com/forecastrss?w={0}&u={1}"
LID_LOOKUP_URL = WEATHER_URL
LID_WEATHER_URL = "http://xml.weather.yahoo.com/forecastrss/{0}_{1}.xml"
WEATHER_NS = "http://xml.weather.yahoo.com/ns/rss/1.0"
GEO_NS = "http://www.w3.org/2003/01/geo/wgs84_pos#"
CONDITION_IMAGE_URL = "http://l.yimg.com/a/i/us/we/52/{0}.gif"
UNITS = {
    "c": {
        "wind": {
            "chill": "°C",
            "direction": "°",
            "speed": "km/h"},
        "atmosphere": {
            "humidity": "%",
            "visibility": "km",
            "pressure": "hPa"},
        "condition": {
            "temp": "°C"},
        "forecast": {
            "low": "°C",
            "high": "°C"},
    },
    "f": {
        "wind": {
            "chill": "°F",
            "direction": "°",
            "speed": "mph"},
        "atmosphere": {
            "humidity": "%",
            "visibility": "mi",
            "pressure": "psi"},
        "condition": {
            "temp": "°F"},
        "forecast": {
            "low": "ˆF",
            "high": "°F"},
    },
}


class Client(object):

    """Interface with the Yahoo! Weather RSS feed.

    Provides methods to search for location data and fetch weather data.

    Methods:
        fetch_lid: fetch a location's LID.
        fetch_woeid: fetch a location's WOEID.
        fetch_weather: fetch a location's weather.

    """

    def fetch_lid(self, woeid):
        """Fetch a location's corresponding LID.

        Args:
            woeid: (string) the location's WOEID.
        
        Returns:
            a string containing the requested LID or None if the LID could
            not be found.

        Raises:
            urllib.error.URLError: urllib.request could not open the URL (Python 3).
            urllib2.URLError: urllib2 could not open the URL (Python 2).
            xml.etree.ElementTree.ParseError: xml.etree.ElementTree failed to parse
                the XML document.

        """
        rss = self._fetch_xml(LID_LOOKUP_URL.format(woeid, "f"))

        # We are pulling the LID from the permalink tag in the XML file
        # returned by Yahoo.

        try:
            link = rss.find("channel/link").text
        except AttributeError:
            return None
        lid = link.split("/forecast/")[1].split("_")[0]
        return lid

    def fetch_weather(self, id, metric=False):
        """Fetch a location's weather.

        *id* can be either a WOEID or LID. The weather data returned for each is
        identical except that the WOEID returns a 2-day forecast and the LID
        returns a 5-day forecast. The LID uses an undocumented API, so use it
        at your own risk.

        Args:
            id: (string) the location's WOEID or LID.
            metric: (bool) return metric data; defaults to False.

        Returns:
            a dict containing the location's weather data or None if
                the weather data couldn't be fetched.

        Raises:
            urllib.error.URLError: urllib.request could not open the URL (Python 3).
            urllib2.URLError: urllib2 could not open the URL (Python 2).
            xml.etree.ElementTree.ParseError: xml.etree.ElementTree failed to parse
                the XML document.

        """

        units = "c" if metric else "f"

        # WOEID is a 32-bit integer, while LID is XXXXNNNN, where X is a letter
        # and N is a number. So, we pick the URL to use based on whether or not
        # the *id* begins with a letter.

        if re.match("^[A-Za-z]", id):
            url = LID_WEATHER_URL.format(id, units)
        else:
            url = WEATHER_URL.format(id, units)

        rss = self._fetch_xml(url)

        if rss.find("channel/item/title").text == "City not found":
            return None

        # xml_items details which tags should be read and what their
        # destination dict key should be. These tags don't appear
        # multiple times.
        # {XML tag: [ElementTree access method, dict key]}

        xml_items = {
            "channel/title": ["text", "title"],
            "channel/link": ["text", "link"],
            "channel/language": ["text", "language"],
            "channel/description": ["text", "description"],
            "channel/lastBuildDate": ["text", "lastBuildDate"],
            "channel/ttl": ["text", "ttl"],
            "channel/image/url": ["text", "logo"],
            "channel/item/guid": ["text", "guid"],
            "channel/{%s}location" % WEATHER_NS:
                ["attrib", "location"],
            # "channel/{%s}units" % WEATHER_NS:
            #     ["attrib", "units"],
            "channel/{%s}wind" % WEATHER_NS:
                ["attrib", "wind"],
            "channel/{%s}atmosphere" % WEATHER_NS:
                ["attrib", "atmosphere"],
            "channel/{%s}astronomy" % WEATHER_NS:
                ["attrib", "astronomy"],
            "channel/item/{%s}condition" % WEATHER_NS:
                ["attrib", "condition"],
        }
        weather = {}
        weather["units"] = UNITS[units]

        for (tag, meta) in xml_items.items():
            if meta[0] == "text":
                try:
                    weather[meta[1]] = rss.find(tag).text
                except AttributeError:
                    weather[meta[1]] = None
            elif meta[0] == "attrib":
                try:
                    weather[meta[1]] = rss.find(tag).attrib
                except AttributeError:
                    weather[meta[1]] = None
            else:
                weather[meta[1]] = None

        try:
            image_url = CONDITION_IMAGE_URL.format(weather["condition"]["code"])
            weather["condition"]["image"] =  image_url
        except (AttributeError, TypeError):
            pass

        try:
            state = weather["atmosphere"]["rising"]
            if state == "0":
                weather["atmosphere"]["state"] = "steady"
            elif state == "1":
                weather["atmosphere"]["state"] = "rising"
            elif state == "2":
                weather["atmosphere"]["state"] = "falling"
            else:
                weather["atmosphere"]["state"] = None
        except (AttributeError, TypeError):
            pass

        weather["forecast"] = []
        try:
            for item in rss.findall(
                    "channel/item/{%s}forecast" % WEATHER_NS):
                weather["forecast"].append(item.attrib)
        except AttributeError:
            weather["forecast"] = None

        weather["geo"] = {}
        try:
            weather["geo"]["lat"] = rss.find(
                "channel/item/{%s}lat" % GEO_NS).text
            weather["geo"]["long"] = rss.find(
                "channel/item/{%s}long" % GEO_NS).text
        except AttributeError:
            weather["geo"] = None

        try:
            weather["wind"]["compass"] = self._degrees_to_direction(
                weather["wind"]["direction"])
        except TypeError:
            pass

        return weather

    def fetch_woeid(self, location):
        """Fetch a location's corresponding WOEID.

        Args:
            location: (string) a location (e.g. 23454 or Berlin, Germany).

        Returns:
            a string containing the location's corresponding WOEID or None if
                the WOEID could not be found.

        Raises:
            urllib.error.URLError: urllib.request could not open the URL (Python 3).
            urllib2.URLError: urllib2 could not open the URL (Python 2).
            xml.etree.ElementTree.ParseError: xml.etree.ElementTree failed to parse
                the XML document.

        """
        rss = self._fetch_xml(
            WOEID_LOOKUP_URL.format(quote(location)))
        try:
            woeid = rss.find("results/Result/woeid").text
        except AttributeError:
            return None
        return woeid

    def _degrees_to_direction(self, degrees):
        """Convert wind direction from degrees to compass direction."""
        try:
            degrees = float(degrees)
        except ValueError:
            return None
        if degrees < 0 or degrees > 360:
            return None
        if degrees <= 11.25 or degrees >= 348.76:
            return "N"
        elif degrees <= 33.75:
            return "NNE"
        elif degrees <= 56.25:
            return "NE"
        elif degrees <= 78.75:
            return "ENE"
        elif degrees <= 101.25:
            return "E"
        elif degrees <= 123.75:
            return "ESE"
        elif degrees <= 146.25:
            return "SE"
        elif degrees <= 168.75:
            return "SSE"
        elif degrees <= 191.25:
            return "S"
        elif degrees <= 213.75:
            return "SSW"
        elif degrees <= 236.25:
            return "SW"
        elif degrees <= 258.75:
            return "WSW"
        elif degrees <= 281.25:
            return "W"
        elif degrees <= 303.75:
            return "WNW"
        elif degrees <= 326.25:
            return "NW"
        elif degrees <= 348.75:
            return "NNW"
        else:
            return None

    def _fetch_xml(self, url):
        """Fetch a url and parse the document's XML."""
        with contextlib.closing(urlopen(url)) as f:
            return xml.etree.ElementTree.parse(f).getroot()
