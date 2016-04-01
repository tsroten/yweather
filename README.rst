yweather
========

About
-----

yweather is a Python module that provides an interface to the `Yahoo! Weather RSS feed <http://developer.yahoo.com/weather/>`_.

International Support
---------------------

.. code:: python

    >>> client.fetch_woeid("Paris, France")
    '615702'
    >>> client.fetch_woeid("Seattle, Washington")
    '2490383'

Location and weather data is not limited to a single country. Fetch data for any location that is available on Yahoo! Weather.

Different countries use different measurement systems (unfortunately). Fetch data according to United States customary units or the metric system.

.. code:: python

    >>> paris_weather = client.fetch_weather("615702", metric=True)
    >>> seattle_weather = client.fetch_weather("2490383", metric=False)

Data is Returned as a Dict
--------------------------

.. code:: python

    >>> norfolk_weather = client.fetch_weather("2460389")
    >>> norfolk_weather["astronomy"]["sunrise"]
    '7:18 am'
    >>> norfolk_weather["condition"]["text"]
    'Partly Cloudy'

Weather data is returned as a Python ``dict``, not as an object of a confusing class.

No API Keys or Signup Needed
----------------------------

Unlike many weather APIs, Yahoo! Weather's RSS feed doesn't require sign ups, API keys, or special authorization to fetch and use their data. All you have to do is follow their `Terms of Use <http://developer.yahoo.com/weather/#terms>`_.

No Manual ID Lookups
--------------------

.. code:: python

    >>> client.fetch_woeid("Raleigh, North Carolina")
    '2478307'
    >>> client.fetch_lid("2379574")
    'USIL0228'

yweather doesn't assume you know location identifiers off the top of your head. You can call the ``fetch_woeid`` or ``fetch_lid`` methods to lookup a location's WOEID or LID. WOEID is Yahoo! Weather's location identifier. LID is The Weather Channel's location identifier.

5-day Forecast Support
----------------------

.. code:: python

    >>> london_weather = client.fetch_weather("UKXX0085")
    >>> len(london_weather["forecast"])
    5

By using a The Weather Channel Location ID (LID), you can fetch a location's 5-day weather forecast. A little warning though -- it's using an undocumented API. If you aren't up for it, you can still get the 2-day forecast using a WOEID.

Documentation
-------------

yweather includes complete and easy-to-read `documentation <https://yweather.readthedocs.org/>`_. Check it out for a gentle introduction or the full API details.

Bug/Issues Tracker
------------------

yweather uses its `GitHub Issues page <https://github.com/tsroten/yweather/issues>`_ to track bugs, feature requests, and support questions.

License
-------

yweather is released under the OSI-approved `MIT License <http://opensource.org/licenses/MIT>`_. See the file LICENSE.txt for more information.
