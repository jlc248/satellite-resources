Low-Earth orbit
===============

JPSS
----

The `Joint Polar Satellite System (JPSS) <https://www.nesdis.noaa.gov/our-satellites/currently-flying/joint-polar-satellite-system>`_ is NOAA's low-earth orbitting satellite program. JPSS satellites circle the Earth from pole to pole and cross the equator about 14 times a day in the afternoon orbit to provide full global coverage twice a day. JPSS data is very important for numerical weather forecasting in the U.S. and deliver critical observations during severe weather events like hurricanes and blizzards. JPSS consists of 5 satellites:

- Suomi NPP
- NOAA 20
- NOAA 21
- JPSS 3 (will be NOAA 22)
- JPSS 4 (will be NOAA 23)

Each satellite has a VIS/IR imager (VIIRS), an IR sounder (CrIS), a microwave sounder (ATMS), and an ozone mapper (OMPS).

.. image:: ../_static/images/JPSS-Constellation-2023.jpg
    :width: 400
    :alt: JPSS constellation cartoon

The bubble chart below lists the different products from JPSS instruments. SDRs are Level-1b reprocessed Sensor Data Records. The SDRs are used as input to produce numerous Environmental Data Record (EDRs), which can be considered "Level-2" products. Most users shouldn't ever have to look at Raw Data Records (RDRs), which are the raw Level-1 data. The figure is courtesy of Amy Huff and Rebekah Esmaili (see `https://github.com/jpss-nodd/python-scripts <https://github.com/jpss-nodd/python-scripts>`_).

.. image:: ../_static/images/JPSS_Products_Bubble_Chart.jpg
    :width: 500
    :alt: Bubble chart with JPSS instrument products

VIIRS
~~~~~

The Visible Infrared Imaging Radiometer Suite, VIIRS, is a scanning radiometer with 5 high-resolution Imagery bands (or I-bands), 16 Moderate resolution bands (M-bands) and a Day/Night band (DNB). The JPSS satellites are in the same orbital plane as NASA's A-Train constellation but at a higher altitude (JPSS altitude is about 824 km). The JPSS satellites are sun synchronous with an equator crossing time of 1330 (local time).

A rotating mirror reflects radiation onto a set of CCD detectors; a single scan relates to a rotation of the mirror. A single VIIRS scan is completed in 1.779 seconds - the mirror rotation rate is slightly faster than the spec but is within tolerance. The M bands and the day/night band have 16 detectors per scan (750 m spatial resolution per pixel), while the I bands have 32 detectors per scan (375 m resolution per pixel).

VIIRS has a swath of about 3040 km in the cross-track direction, while MODIS has a swath width of 2330 km. With VIIRS, there are no coverage gaps in the Tropics as there are with MODIS.

This table helps summarize the VIIRS channels.

+-------------+---------------------+------------------+---------------+
| Band Number |  Central Wavelength | Nadir Resolution | Gain          |
+=============+=====================+==================+===============+
|    I-1      |   0.640 µm          |   375 m          | single        |
+-------------+---------------------+------------------+---------------+
|    I-2      |   0.865 µm          |   375 m          | single        |
+-------------+---------------------+------------------+---------------+
|    I-3      |   1.61 µm           |   375 m          | single        |
+-------------+---------------------+------------------+---------------+
|    I-4      |   3.74 µm           |   375 m          | single        |
+-------------+---------------------+------------------+---------------+
|    I-5      |   11.45 µm          |   375 m          | single        |
+-------------+---------------------+------------------+---------------+
|    M-1      |   0.412 µm          |   750 m          | dual          |
+-------------+---------------------+------------------+---------------+
|    M-2      |   0.445 µm          |   750 m          | dual          |
+-------------+---------------------+------------------+---------------+
|    M-3      |   0.488 µm          |   750 m          | dual          |
+-------------+---------------------+------------------+---------------+
|    M-4      |   0.555 µm          |   750 m          | dual          |
+-------------+---------------------+------------------+---------------+
|    M-5      |   0.672 µm          |   750 m          | dual          |
+-------------+---------------------+------------------+---------------+
|    M-6      |   0.746 µm          |   750 m          | single        |
+-------------+---------------------+------------------+---------------+
|    M-7      |   0.865 µm          |   750 m          | dual          |
+-------------+---------------------+------------------+---------------+
|    M-8      |   1.24 µm           |   750 m          | single        |
+-------------+---------------------+------------------+---------------+
|    M-9      |   1.38 µm           |   750 m          | single        |
+-------------+---------------------+------------------+---------------+
|    M-10     |   1.61 µm           |   750 m          | single        |
+-------------+---------------------+------------------+---------------+
|    M-11     |   2.25 µm           |   750 m          | single        |
+-------------+---------------------+------------------+---------------+
|    M-12     |   3.70 µm           |   750 m          | single        |
+-------------+---------------------+------------------+---------------+
|    M-13     |   4.05 µm           |   750 m          | dual          |
+-------------+---------------------+------------------+---------------+
|    M-14     |   8.55 µm           |   750 m          | single        |
+-------------+---------------------+------------------+---------------+
|    M-15     |   10.76 µm          |   750 m          | single        |
+-------------+---------------------+------------------+---------------+
|    M-16     |   12.01 µm          |   750 m          | single        |
+-------------+---------------------+------------------+---------------+
|    DNB      |   0.7 µm            |   500 m          | multiple      |
+-------------+---------------------+------------------+---------------+

Geolocation files
,,,,,,,,,,,,,,,,,

Geolocation files are produced separately. Here are their codes:

* I-band SDR geolocation files

  * GIMGO: projected onto smooth ellipsoid (WGS84 ellipsoid)

  * GITCO: parallax-corrected for terrain

* M-band SDR geolocation files

  * GMODO: projected onto smooth ellipsoid

  * GMTCO: parallax-corrected for terrain

* Day/Night Band geolocation file

  * GDNBO: projected onto smooth ellipsoid 

* EDR geolocation files (use ground-track Mercator projection)

  * GIGTO: I-band EDR geolocation

  * GMGTO: M-band EDR geolocation

  * GNCCO: Day/Night Band EDR (NCC) geolocation


.. seealso::

  * `VIIRS Imagery EDR User's Guide <https://rammb.cira.colostate.edu/projects/npp/VIIRS_Imagery_EDR_Users_Guide.pdf>`_
  * `VIIRS ATBD <https://www.star.nesdis.noaa.gov/jpss/documents/ATBD/D0001-M01-S01-003_JPSS_ATBD_VIIRS-SDR_E.pdf>`_

Data Viewing
,,,,,,,,,,,,

* `CIRA Slider <https://rammb-slider.cira.colostate.edu/?sat=jpss&sec=northern_hemisphere&x=14976&y=16544&z=0&angle=0&im=12&ts=1&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&mhidden%5Bborders%5D=1&p%5B0%5D=cira_geocolor&opacity%5B0%5D=1&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6>`_
* `VIIRS Today <https://ge.ssec.wisc.edu/viirs-today/>`_

Data Access
,,,,,,,,,,,

* `NASA LAADS <https://ladsweb.modaps.eosdis.nasa.gov/search/>`_

  * Can search by dataset, time, and location

* University of Wisconsin `SIPS <https://sips.ssec.wisc.edu/products>`_

* `NOAA Open Data Dissemination -- JPSS <https://registry.opendata.aws/noaa-jpss/>`_

.. seealso::

  * https://github.com/jpss-nodd/python-scripts

    * For downloading and visualizing JPSS VIIRS data

CrIS
~~~~

ATMS
~~~~

NUCAPS
~~~~~~

MetOp
-----

Oribt tracks
------------

The University of Wisconsin -- Madison Space Science and Engineering Center provides a resource to see `historical and future tracks <https://www.ssec.wisc.edu/datacenter/polar_orbit_tracks/>`_ (next few days) for many polar-orbitting satellites.

.. image:: ../_static/images/NPP_tracks.gif
  :width: 1000
  :alt: Map with orbit tracks for Suomi-NPP.
