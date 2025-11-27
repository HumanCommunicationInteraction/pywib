Movement Metrics
================

.. currentmodule:: pywib

Velocity
--------
The velocity is the rate of change of position with respect to time. Commonly used to analyze the speed of movement during user interactions :cite:p:`Kieslich2019-mt, Katerina2018-ch`.

The function :py:func:`~pywib.velocity` computes the velocity based on the distance and time difference between consecutive points.
The velocity is calculated as:

.. |xi| replace:: :math:`x_i`
.. |yi| replace:: :math:`y_i`
.. |ti| replace:: :math:`t_i`
.. |i| replace:: :math:`i`

.. math::

   v_i = \frac{\sqrt{(x_{i} - x_{i-1})^2 + (y_{i} - y_{i-1})^2}}{t_{i} - t_{i-1}}

where (|xi|, |yi|) are the coordinates and (|ti|) is the timestamp of point (|i|).

The function :py:func:`~pywib.velocity_metrics` computes velocity metrics such as mean, max, and min of the velocity for each session.


Acceleration
------------
The acceleration is the rate of change of velocity with respect to time, which provides insights into how quickly users change their speed during interactions :cite:p:`Kieslich2019-mt,Katerina2018-ch`.

The function :py:func:`~pywib.acceleration` computes the acceleration based on the change in velocity over time from a DataFrame or session traces.

The acceleration is calculated as:

.. |vi| replace:: :math:`v_i`
.. math::

   a_i = \frac{v_{i} - v_{i-1}}{t_{i} - t_{i-1}}

where \(|vi|\) is the velocity at point \(|i|\) and \(|ti|\) is the timestamp of point \(|i|\).

Maximum, minimum, and mean acceleration metrics for each session can be computed using the function :py:func:`~pywib.acceleration_metrics`.

Jerkiness
---------

The function :py:func:`~pywib.jerkiness` computes the jerkiness of interaction points from a DataFrame or session traces, based on the change in acceleration over time.

The jerkiness is calculated as the change in acceleration per unit time:

.. |ai| replace:: :math:`a_i`
.. math::

   j_i = \frac{a_{i} - a_{i-1}}{t_{i} - t_{i-1}}

where \(|ai|\) is the acceleration at point \(|i|\) and \(|ti|\) is the timestamp of point \(|i|\).

The function :py:func:`~pywib.jerkiness_metrics` computes jerkiness metrics such as mean, max, and min jerkiness for each session.

Path
----
The path or total distance traveled during user interactions is a key metric for analyzing movement efficiency :cite:p:`Kieslich2019-mt,Katerina2018-ch`.

The function :py:func:`~pywib.path` calculates the path length for interaction points from a DataFrame or session traces.
This function computes the path length based on the Euclidean distance between consecutive points.

The distance between consecutive points is calculated as:

.. math::

   d_i = \sqrt{(x_{i} - x_{i-1})^2 + (y_{i} - y_{i-1})^2}

AUC Ratio
---------
The Area Under the Curve (AUC) is a metric that quantifies the overall movement efficiency during user interactions :cite:p:`Kieslich2019-mt,Katerina2018-ch`

The function :py:func:`~pywib.auc_ratio` calculates the AUC ratio for each session.

That is, the real area under the curve and the optimal area (straight-line) and returns the ratio between their difference and the rael area.

.. |A_real| replace:: :math:`A_{real}`
.. |A_opt| replace:: :math:`A_{opt}`


Given the real area |A_real| and the optimal area |A_opt| the AUC ratio is computed as:

.. math::

   AUC Ratio = \frac{|A_{real} - A_{opt}|}{|A_{opt}| + 10^{-6}}

This small epsilon prevents division-by-zero when the optimal area is 0.

Metrics are also provided via :py:func:`~pywib.auc_ratio_metrics`, which computes mean, max, and min AUC and AUC ratio for each session.

Reference
---------

For more information on geometric features of drag-and-drop trajectories, see:

- `Using Geometric Features of Drag-and-Drop Trajectories to Understand Students Learning <https://dl.acm.org/doi/10.1145/3544548.3581143>`_.

.. bibliography::