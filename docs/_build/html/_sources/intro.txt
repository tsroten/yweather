Introduction
============

This is the documentation for :mod:`yweather`. :mod:`yweather` is a Python module that provides an interface to the `Yahoo! Weather RSS feed <http://developer.yahoo.com/weather/>`_

Prerequisites
-------------

:mod:`yweather` requires Python 2.6, 2.7, or 3 to run.

Installation
------------

There are multiple ways to install :mod:`yweather`. If you are unsure about which method to use, try ``pip``.

pip (recommended)
~~~~~~~~~~~~~~~~~

`pip <http://www.pip-installer.org/>`_ is a tool for installing and managing Python packages. To install :mod:`yweather`, run:

.. code-block:: bash

    $ pip install yweather

This will download :mod:`yweather` from `the Python Package Index <http://pypi.python.org/>`_ and install it in your Python's ``site-packages`` directory.

Tarball Release
~~~~~~~~~~~~~~~

1. Download the most recent release from `yweather's PyPi page <http://pypi.python.org/pypi/yweather/>`_.
2. Unpack the tarball.
3. From inside the ``yweather-0.X`` directory, run ``python setup.py install``

This will install :mod:`yweather` in your Python's ``site-packages`` directory.

Install the Development Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`yweather's code <https://github.com/tsroten/yweather>`_ is hosted at GitHub. To install the development version, do the following:

1. Make sure `Git <http://git-scm.org/>`_ is installed. Test if it's installed by running ``git --version``
2. ``git clone git://github.com/tsroten/yweather.git``
3. ``pip install -e yweather``

This will link the ``yweather`` directory into your ``site-packages`` directory. You can find out where your ``site-packages`` directory is by running:

.. code-block:: bash

    python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"

Basic Usage
-----------

.. code-block:: python

    >>> import yweather
    >>> client = yweather.Client()
    >>> client.fetch_woeid("Oslo, Norway")
    '862592'
    >>> oslo_weather = client.fetch_weather("862592")
    >>> oslo_weather["atmosphere"]["pressure"]
    '30.24'
    >>> oslo_weather["condition"]["text"]
    'Mostly Cloudy'

This code creates a :class:`yweather.Client` instance that allows you to fetch a location's :term:`WOEID` and weather. The weather data is returned as a :class:`dict <python3:dict>`.
    
