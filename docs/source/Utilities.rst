Utilities
=========

This section provides examples and utilities for some common problems. The source code is found in the ``src`` directory of this repo.

Parallax correction
-------------------

For geostationary satellite data in particular, the affects of parallax are a big issue. Because the Earth is (nearly) round and geostationary satellites are very far away ( ), the apparent position of objects above the surface of the earth (such as clouds) can be considerably displaced from their actual ground-relative location. This displacement is a function of the position of the cloud relative to the satellite (i.e., the satellite-viewing angle) and a function of the height of the cloud above the surface of the Earth. These figures from the University of Wyoming help to illustrate. 

.. image:: ../_static/parallax_1.gif
    :width: 400
    :alt: Schematic diagram showing effects of parallax

A geostationary satellite's nadir point is at the equator. At this point, high clouds and low clouds have no displacement. But everywhere else, high clouds are displaced more than low clouds. Comparing the high cloud and low cloud in approximately the mid-latitudes, we can see that the cloud edge closer to the equator is displaced much further poleward (i.e., away from the satellite) for the high cloud than the low cloud. In this example, assuming an 18-km cloud top and a 3-km cloud top at a viewing angle of 52 degrees, the parallax displacements are 30 km and 5 km, respectively. Moving that same low cloud closer to the pole, the parallax displacement accelerates quickly.

.. image:: ../_static/parallax_2.png
    :width: 400
    :alt: Graph of normalized cloud offset as a function of the angular distance from nadir.

From this graph, we can see that the normalized cloud offset increases exponentially as the angular distance from nadir increases. For example, for a cloud top at 10 km AGL, and a satellite-viewing angle 60 degrees, the displacement is ``10 * 2.6 = 26 km``.

Solar-zenith angle
------------------

Satellite-viewing angle
-----------------------
