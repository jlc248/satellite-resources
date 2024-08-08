Geostationary
=============

.. _installation:

GOES-R
------

The `Geostationary Operational Environment Satellite R-Series <https://www.goes-r.gov/>`_ is NOAA's latest geostationary set of satellites. GOES-16, GOES-17, GOES-18, and GOES-19 are part of this series. The two instruments for terrestrial weather are the `Advanced Baseline Imager (ABI) <https://www.earthdata.nasa.gov/sensors/abi>`_ and the `Geostationary Lightning Mapper (GLM) <https://www.earthdata.nasa.gov/sensors/glm>`_.

.. image:: ../static/images/GOES-East_geosphere.png
  :width: 500
  :alt: GOES-East full disk true-color image.

Advanced Baseline Imager (ABI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ABI consists of 16 channels and passively senses data from visible, near-infrared, and longwave-infrared parts of the EM spectrum. The table summarizes some characteristics of the bands.

.. image:: ../static/images/ABI_table.png
  :width: 500
  :alt: Table with ABI band characteristics

Geostationary Lightning Mapper (GLM)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
