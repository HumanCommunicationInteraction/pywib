Introduction
============

Welcome to **pywib** (Python Web Interaction Behaviour) the python library designed to help ease the analysis of user interaction data in the field of HCI (Human-Computer Interaction).

This project aims to analyze user interaction with web applications by processing interaction event data (such as clicks, mouse movements, scrolls, etc.) recorded by researchers to aid their studies.

It provides tools to compute various interaction related metrics (like velocity, acceleration, auc, etc.) and other useful functionalities to facilitate the analysis of user behavior, such as stroke visualization or video generation of user sessions.



Installation
-------------
You can install **pywib** using pip:

.. code-block:: bash

   pip install pywib

Getting Started
-----------------

I suggest you take a deep look at rest of the documentation, such as the `Keyboard Interaction Metrics <keyboard.html>`_ or `Movement Interaction Metrics <movement.html>`_ sections in order to understand the different metrics that can be computed with **pywib** and find those that suit your research.

After that, you can check the `API Reference <api/index.html>`_ for more detailed information about the available functions and classes.

Small Example
~~~~~~~~~~~~~~
.. code-block:: python

   from pywib import velocity, velocity_metrics

   v = velocity(df_all_sessions)
   v_metrics = velocity_metrics(None, v)
