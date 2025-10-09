Movement Metrics
=============

.. currentmodule:: pywib

Velocity
--------
See the function implementation in :py:func:`pywib.velocity`.

This function computes the velocity based on the distance and time difference between consecutive points.
The velocity is calculated as:

.. |xi| replace:: :math:`x_i`
.. |yi| replace:: :math:`y_i`
.. |ti| replace:: :math:`t_i`
.. |i| replace:: :math:`i`

.. math::

   v_i = \frac{\sqrt{(x_{i} - x_{i-1})^2 + (y_{i} - y_{i-1})^2}}{t_{i} - t_{i-1}}

where (|xi|, |yi|) are the coordinates and (|ti|) is the timestamp of point (|i|).

The function :py:func:`pywib.velocity_metrics` computes velocity metrics such as mean, max, and min for each session.


Acceleration
------------
See the function implementation in :py:func:`pywib.acceleration`.

This function computes the acceleration based on the change in velocity over time from a DataFrame or session traces.
Note: the input DataFrame/traces must contain computed 'velocity' and 'dt' columns (where 'dt' is the time difference between consecutive samples).

The acceleration is calculated as:


.. |vi| replace:: :math:`v_i`
.. math::

   a_i = \frac{v_{i} - v_{i-1}}{t_{i} - t_{i-1}}

where \(|vi|\) is the velocity at point \(|i|\) and \(|ti|\) is the timestamp of point \(|i|\).

Jerkiness
---------

Calculates the jerkiness of interaction points from a DataFrame or session traces.
This function computes the jerkiness based on the change in acceleration over time.
Note: the input DataFrame/traces must contain computed 'acceleration' and 'dt' columns (where 'dt' is the time difference between consecutive samples).

The jerkiness is calculated as the change in acceleration per unit time:

.. |ai| replace:: :math:`a_i`
.. math::

   j_i = \frac{a_{i} - a_{i-1}}{t_{i} - t_{i-1}}

where \(|ai|\) is the acceleration at point \(|i|\) and \(|ti|\) is the timestamp of point \(|i|\).

Path
----

Calculates the path length for interaction points from a DataFrame or session traces.
This function computes the path length based on the Euclidean distance between consecutive points.

The distance between consecutive points is calculated as:

.. math::

   d_i = \sqrt{(x_{i} - x_{i-1})^2 + (y_{i} - y_{i-1})^2}

AUC Ratio
---------

Calculates the AUC ratio for each session. This function computes the real area under the curve and the optimal area (straight-line) and returns the ratio between their difference and the optimal area.

.. |A_real| replace:: :math:`A_{real}`
.. |A_opt| replace:: :math:`A_{opt}`


Given the real area |A_real| and the optimal area |A_opt| the AUC ratio is computed as:

.. math::

   r = \frac{|A_{real} - A_{opt}|}{|A_{opt}| + 10^{-6}}

This small epsilon prevents division-by-zero when the optimal area is 0.

Reference
---------

For more information on geometric features of drag-and-drop trajectories, see:

- `Using Geometric Features of Drag-and-Drop Trajectories to Understand Students Learning <https://dl.acm.org/doi/10.1145/3544548.3581143>`_.
