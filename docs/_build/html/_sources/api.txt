API
===

.. py:module:: yweather

.. data:: WOEID_LOOKUP_URL
    
    The URL used to fetch a location's corresponding :term:`WOEID`.

.. data:: WEATHER_URL

    The URL used to fetch a :term:`WOEID`'s weather.

.. data:: LID_LOOKUP_URL

    The URL used to fetch a location's corresponding :term:`LID`.

.. data:: LID_WEATHER_URL

    The URL used to fetch a :term:`LID`'s weather.

.. data:: WEATHER_NS

    The XML namespace used in the weather RSS feed.

.. data:: GEO_NS

    The XML namespace used for the lat/long coordinates in the RSS feed.

.. data:: CONDITION_IMAGE_URL

    The URL of an image depicting the current conditions.

.. data:: UNITS

    A :class:`dict <python3:dict>` that maps data names to units.

.. class:: Client()

    Interface with the Yahoo! Weather RSS feed. Provides methods to search for location data and fetch weather data.

    .. method:: fetch_lid(woeid)

        Fetch a location's corresponding :term:`LID`.

        :param woeid: the location's :term:`WOEID`.
        :type woeid: :mod:`string <python3:string>`
        :returns: a :mod:`string <python3:string>` containing the requested :term:`LID` or :data:`None <python3:None>` if the :term:`LID` could not be found.
        :raises urllib.error.URLError: :mod:`urllib.request <python3:urllib.request>` could not open the URL (Python 3).
        :raises urllib2.URLError: :mod:`urllib2 <python2:urllib2>` could not open the URL (Python 2).
        :raises xml.etree.ElementTree.ParseError: :mod:`xml.etree.ElementTree <python3:xml.etree.ElementTree>` failed to parse the XML document.

    .. method:: fetch_weather(id[, metric=False])

        Fetch a location's weather.

        *id* can be either a :term:`WOEID` or :term:`LID`. The weather data returned for each is identical except that the :term:`WOEID` returns a 2-day forecast and the :term:`LID` returns a 5-day forecast. The :term:`LID` uses an undocumented API, so use it at your own risk.

        The returned data is a :class:`dict <python3:dict>` with the requested weather data. It loosely follows the `Yahoo! Weather RSS feed response structure <http://developer.yahoo.com/weather/#response>`_, but has some noticeable differences. The following table outlines the data structure.

        ============== ========== ============ =====
        Keys           ..         ..           Value
        ============== ========== ============ =====
        title                                  The title of the feed, which includes the location city. For example "Yahoo! Weather - Sunnyvale, CA".
        link                                   The URL of the forecast for  this location.
        language                               The language of the weather forecast, for example, en-us for US English.
        description                            The overall description of the feed including the location, for example "Yahoo! Weather for Sunnyvale, CA".
        lastBuildDate                          The last time the feed was updated. For example, Fri, 04 Jan 2013 6:56 am PST.
        ttl                                    Time to Live; how long in minutes this feed should be cached.
        logo                                   The URL for the Yahoo! Weather logo associated with this feed.
        guid                                   Unique identifier for the forecast, made up of the location ID, the date, and the time.
        location       city                    city name
        location       region                  state, territory, or region, if given.
        location       country                 two-character country code
        geo            lat                     The latitude of the location.
        geo            long                    The longitude of the location.
        units          wind       chill        °F or °C
        units          wind       direction    °
        units          wind       speed        mph or km/h
        units          atmosphere humidity     %
        units          atmosphere visbility    mi or km
        units          atmosphere pressure     psi or hPa
        units          condition  temp         °F or °C
        units          forecast   low          °F or °C
        units          forecast   high         °F or °C
        wind           chill                   wind chill in degrees
        wind           direction               wind direction, in degrees
        wind           compass                 wind direction, according to a compass. For example, NNW, SE, or W.
        wind           speed                   wind speed in mph or km/h
        atmosphere     humidity                humidity, in percent
        atmosphere     visibility              visibility, in mi or km.
        atmosphere     pressure                barometric pressure in psi or hPa.
        atmosphere     rising                  state of the barometric pressure as a number: 0 (steady), 1 (rising), or 2 (falling).
        atmosphere     state                   state of the barometric pressure as text: steady, rising, or falling.
        astronomy      sunrise                 today's sunrise time. The time is in a local time format of "h:mm am/pm", for example "7:02 am"
        astronomy      sunset                  today's sunset time. The time is in a local time format of "h:mm am/pm", for example "4:51 pm".
        condition      text                    a textual description of conditions, for example, "Partly Cloudy"
        condition      code                    the condition code for this forecast. Yahoo! Weather's developer network lists the `possible values <http://developer.yahoo.com/weather/#codes>`_.
        condition      image                   the URL of an image that depicts the current conditions (clouds, sun, rain, etc.).
        condition      temp                    the current temperature in °F or °C
        condition      date                    the current date and time for which this forecast applies. For example, Fri, 04 Jan 2013 6:56 am PST.
        forecast                               contains a :class:`list <python3:list>`, where each item is a :class:`dict <python3:dict>` that contains the weather forecast for a specific day.
        --             day                     day of the week to which this forecast applies. Possible values are Mon Tue Wed Thu Fri Sat Sun
        --             date                    the date to which this forecast applies. The date is in "dd Mmm yyyy" format, for example "3 Nov 2005"
        --             low                     the forecasted low temperature for this day in °F or °C
        --             high                    the forecasted high temperature for this day in °F or °C
        --             text                    a textual description of conditions, for example, "Partly Cloudy"
        --             code                    the condition code for this forecast. Yahoo! Weather's developer network lists the `possible values <http://developer.yahoo.com/weather/#codes>`_.
        ============== ========== ============ =====

        The differences between this data structure and Yahoo! Weather's are:
            * *units* breaks down the data units further and uses more helpful key names.
            * *logo* represents the RSS feed's ``<image>`` tag.
            * *guid* was moved to the top level.
            * *condition* has the *image* key, which provides easy access to a URL of an image depicting the current sky conditions.
            * *atmosphere* has the *state* key, which gives a textual description of the barometric pressure state.
            * *geo* is now a :class:`dict <python3:dict>` with *lat* and *long* keys.
            * *wind* includes the *compass* key, which provides wind direction according to a compass (e.g. NNW, SE, or W).

        Example usage of the returned :class:`dict <python3:dict>`:

        .. code-block:: python

            >>> print result["wind"]["compass"]
            NNW
            >>> print result["atmosphere"]["pressure"], result["units"]["atmosphere"]["pressure"]
            29.95 psi
            >>> print len(result["forecast"])
            2
            >>> print result["forecast"][0]["text"]
            Partly Cloudy

        :param id: the location's :term:`WOEID` or :term:`LID`.
        :type id: :mod:`string <python3:string>`
        :param metric: return metric data; defaults to :data:`False <python3:False>`.
        :type metric: :func:`bool <python3:bool>`
        :returns: a :class:`dict <python3:dict>` containing the location's weather data or :data:`None <python3:None>` if the weather data couldn't be fetched.
        :raises urllib.error.URLError: :mod:`urllib.request <python3:urllib.request>` could not open the URL (Python 3).
        :raises urllib2.URLError: :mod:`urllib2 <python2:urllib2>` could not open the URL (Python 2).
        :raises xml.etree.ElementTree.ParseError: :mod:`xml.etree.ElementTree <python3:xml.etree.ElementTree>` failed to parse the XML document.
    
    .. method:: fetch_woeid(location)

        Fetch a location's corresponding :term:`WOEID`.

        :param location: a location (e.g. 23454 or Berlin, Germany).
        :type location: :mod:`string <python3:string>`
        :returns: a :mod:`string <python3:string>` containing the requested :term:`WOEID` or :data:`None <python3:None>` if the :term:`WOEID` could not be found.
        :raises urllib.error.URLError: :mod:`urllib.request <python3:urllib.request>` could not open the URL (Python 3).
        :raises urllib2.URLError: :mod:`urllib2 <python2:urllib2>` could not open the URL (Python 2).
        :raises xml.etree.ElementTree.ParseError: :mod:`xml.etree.ElementTree <python3:xml.etree.ElementTree>` failed to parse the XML document.
