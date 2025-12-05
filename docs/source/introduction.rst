Introducción
============

Welcome to **pywib** (Python Web Interaction Behaviour).

This proyect aims to analyze user interaction with web applications by processing interaction event data (such as clicks, mouse movements, scrolls, etc.) recorded in CSV files.
It provides tools to compute various movement metrics (like velocity, acceleration, jerkiness, etc.) and others such as visualizing interaction traces.


Installation
-------------
You can install **pywib** using pip:

.. code-block:: bash

   pip install pywib

Getting Started
-----------------

.. code-block:: Python

   from pywib import velocity, velocity_metrics

   v = velocity(df_all_sessions)
   v_metrics = velocity_metrics(None, v)
