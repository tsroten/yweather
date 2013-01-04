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

"""

try:
    from urllib.request import urlopen
    from urllib.parse import quote
except ImportError:
    from urllib2 import urlopen
    from urllib import quote
import contextlib
import xml.etree.ElementTree


WOEID_LOOKUP_URL = ("http://locdrop.query.yahoo.com/v1/public/yql?"
                    "q=select%20woeid%20from%20locdrop.placefinder%20"
                    "where%20text='{0}'")


class Client(object):

    """Interface with the Yahoo! Weather RSS feed.

    Provides methods to search for location data and fetch weather data.

    Methods:
        fetch_woeid: fetch a location's WOEID.

    """

    def fetch_woeid(self, location):
        """Fetch a location's corresponding WOEID.

        Args:
            location: (str) a location (e.g. 23454 or Berlin, Germany).

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

    def _fetch_xml(self, url):
        """Fetch a url and parse the document's XML."""
        with contextlib.closing(urlopen(url)) as f:
            return xml.etree.ElementTree.parse(f).getroot()
