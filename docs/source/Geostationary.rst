Geostationary
=============

.. _installation:

GOES-R
------

The `Geostationary Operational Environment Satellite R-Series <https://www.goes-r.gov/>`_ is NOAA's latest geostationary set of satellites. GOES-16, GOES-17, GOES-18, and GOES-19 are part of this series. The two instruments for terrestrial weather are the `Advanced Baseline Imager (ABI) <https://www.goes-r.gov/spacesegment/abi.html>`_ and the `Geostationary Lightning Mapper (GLM) <https://www.goes-r.gov/spacesegment/glm.html>`_.

.. image:: ../static/images/GOES-East_geosphere.png
  :width: 500
  :alt: GOES-East full disk true-color image.

Advanced Baseline Imager (ABI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ABI consists of 16 channels and passively senses data from visible, near-infrared, and longwave-infrared parts of the EM spectrum. The table summarizes some characteristics of the bands.

.. image:: ../static/images/ABI_table.png
  :width: 500
  :alt: Table with ABI band characteristics

Modes and sectors
,,,,,,,,,,,,,,,,,

ABI has multiple scan modes. In mode 4, or continuous full disk mode, the ABI produces a full disk (Western Hemisphere) image every five minutes. In mode 3, or flex mode, the ABI concurrently produces a full disk every 15 minutes, a CONUS image (resolution 3000 km by 5000 km) every five minutes, and two mesoscale domains (resolution 1000 km by 1000 km at the satellite sub-point) every 60 seconds or one sub-domain every 30 seconds. Mode 6, or 10-minute flex mode, which became the default operating mode for GOES-16 and GOES-17 in April 2019, provides a full disk image every 10 minutes, a CONUS (GOES-16) / PACUS (GOES-17) image every five minutes, and images from both mesoscale domains every 60 seconds (or one sub-domain every 30 seconds). All ABI bands have on-orbit calibration.

The pair of images below shows the increasing pixel area further away from nadir. The default east position is at 75 deg west longitude; the default west position is at 137 deg west longitude. Within the full-disk image, there is outlined the CONUS/PACUS and mesoscale sector domains. 

.. image:: ../static/images/GOES_pixel-areas.png
  :width: 800
  :alt: Two images with GOES pixel areas and sector boxes.

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
