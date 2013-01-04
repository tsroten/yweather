API
===

.. py:module:: yweather

.. data:: WOEID_LOOKUP_URL
    
    The URL used to fetch a location's corresponding :term:`WOEID`.

.. class:: Client()

    Interface with the Yahoo! Weather RSS feed. Provides methods to search for location data and fetch weather data.
    
    .. method:: fetch_woeid(location)

        Fetch a location's corresponding :term:`WOEID`.

        :param location: a location (e.g. 23454 or Berlin, Germany).
        :type location: :mod:`string <python3:string>`
        :returns: a :mod:`string <python3:string>` containing the requested :term:`WOEID` or :data:`None <python3:None>` if the :term:`WOEID` could not be found.
        :raises urllib.error.URLError: :mod:`urllib.request <python3:urllib.request>` could not open the URL (Python 3).
        :raises urllib2.URLError: :mod:`urllib2 <python2:urllib2>` could not open the URL (Python 2).
        :raises xml.etree.ElementTree.ParseError: :mod:`xml.etree.ElementTree <python3:xml.etree.ElementTree>` could not open the URL.
