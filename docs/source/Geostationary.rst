Geostationary
=============

.. _installation:

GOES-R
------

The Geostationary Operational Environment Satellite R-Series is NOAA's latest geostationary set of satellites. GOES-16, GOES-17, GOES-18, and GOES-19 are part of this series.

.. image:: docs/static/GOES-East_geosphere.png
  :width: 500
  :alt: GOES-East full disk true-color image.

Creating recipes
----------------

To retrieve a list of random ingredients,
you can use the ``lumache.get_random_ingredients()`` function:

.. autofunction:: lumache.get_random_ingredients

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
will raise an exception.

.. autoexception:: lumache.InvalidKindError

For example:

>>> import lumache
>>> lumache.get_random_ingredients()
['shells', 'gorgonzola', 'parsley']
