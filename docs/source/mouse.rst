Mouse Metrics
=================

.. currentmodule:: pywib

Clicks
------
From a dataset of mouse interaction points, there are several click-related metrics that can be computed to analyze user behavior and interaction patterns.

Two common click metrics are:

1. **Number of Clicks**: This metric counts the total number of clicks recorded during a session. See the function implementation in :py:func:`~pywib.number_of_clicks`.
2. **Click Slip**: This metric measures the deviation of click positions from the intended targets, providing insights into user accuracy. See the function implementation in :py:func:`~pywib.click_slip`.
3. **Click Duration**: This metric measures the time duration of each click action, providing insights into user interaction speed. See the function implementation in :py:func:`~pywib.click_duration`.
