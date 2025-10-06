API Reference
=============

.. currentmodule:: pywib

Velocity
--------

Calculates the velocity of interaction points from a DataFrame or session traces.
This function computes the velocity based on the distance and time difference between consecutive points.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - df
     - pd.DataFrame
     - DataFrame containing the columns 'x', 'y', and 'timeStamp'.
   * - traces
     - dict[str, list[pd.DataFrame]]
     - Dictionary with keys as sessionId and values as lists of DataFrames. If None, traces will be computed from df.

Returns
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Return
     - Type
     - Description
   * - result
     - dict
     - Dictionary with keys as sessionId and values as DataFrames with an additional 'velocity' column.

Velocity formula
~~~~~~~~~~~~~~~~

The velocity is calculated as:

.. math::

   v_i = \frac{\sqrt{(x_{i} - x_{i-1})^2 + (y_{i} - y_{i-1})^2}}{t_{i} - t_{i-1}}

where \(x_i, y_i\) are the coordinates and \(t_i\) is the timestamp of point \(i\).

Reference
~~~~~~~~~~

For more information on geometric features of drag-and-drop trajectories, see:

- 'Using Geometric Features of Drag-and-Drop Trajectories to Understand Students' Learning <https://github.com/HumanCommunicationInteraction/pywib/issues/3#:~:text=Using%2>
