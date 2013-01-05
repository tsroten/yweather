Usage
=====

Let's learn how to use :mod:`yweather`.

Create a :class:`~yweather.Client` Object
-----------------------------------------

:mod:`yweather` consists of a single class, :class:`~yweather.Client`.

.. code-block:: python

    >>> import yweather
    >>> client = yweather.Client()

By creating an instance of :class:`~yweather.Client`, you've created an object that you can use to fetch location identifiers and weather data from Yahoo! Weather.

Fetch a Location's :term:`WOEID`
--------------------------------

Yahoo! Weather gives every location a unique :term:`WOEID`. In order to fetch weather data from Yahoo!, you must first know the location's :term:`WOEID`.

.. code-block:: python

    >>> client.fetch_woeid("Beijing, China")
    '2151330'
    >>> client.fetch_woeid("96734")
    '12798281'
    >>> client.fetch_woeid("10 South Main Street, Harrisonburg, VA")
    '12767058'

You can retrieve a :term:`WOEID` by passing a general or specific address. The above example used city and country, ZIP code, and complete address.

Fetch a Location's Weather
--------------------------

Once you have a location's :term:`WOEID`, you can use it to fetch the location's weather. Weather data is returned as a :class:`dict <python3:dict>`. Its structure is detailed in :meth:`~yweather.Client.fetch_weather`'s API documentation.

.. code-block:: python

    >>> beijing_weather = client.fetch_weather("2151330")
    >>> beijing_weather["guid"]
    'CHXX0008_2013_01_06_7_00_CST'
    >>> beijing_weather["description"]
    'Yahoo! Weather for Beijing, CN'
    >>> beijing_weather["condition"]["temp"]
    '28'

The returned :class:`dict <python3:dict>` contains metadata along with the weather data itself. By default, :term:`United States customary units` are used, but by changing the *metric* argument, you can receive data according to the :term:`metric system`.

.. code-block:: python

    >>> kailua_weather = client.fetch_weather("12798281", metric=True)
    >>> kailua_weather["forecast"][0]["high"]
    '25'
    >>> kailua_weather["units"]["forecast"]["high"]
    '°C'

The units used for each data value are accessible with the *units* key.

Using a Location's :term:`LID`
------------------------------

Because Yahoo! Weather's data comes from `The Weather Channel <http://www.weather.com>`_, weather data is also accessible via a The Weather Channel :term:`LID`. This provides access to a 5-day forecast versus the 2-day forecast available with a location's :term:`WOEID`.

.. code-block:: python

    >>> client.fetch_lid("2151330")
    'CHXX0008'
    >>> beijing_weather = client.fetch_weather("CHXX0008")
    >>> len(beijing_weather["forecast"])
    5

The :meth:`~yweather.Client.fetch_lid` method takes a :term:`WOEID` and returns a :term:`LID`. You can pass the :term:`LID` to the :meth:`~yweather.Client.fetch_weather` method.
