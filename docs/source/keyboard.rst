Kestroke Metrics
================

.. currentmodule:: pywib

Introduction
-------------
    "*Keystroke dyanmics is the study of the unique timing patterns in an indiviual's typing, and typically includes extracting keystroke timing features such as the duration of a key press and the time elapsed between key presses.*" :cite:p:`Epp2011-rj` 

This metrics (or dyanmics) obtained from keyboard interaction have been widely used in various applications, including user authentication, behavioral biometrics, affective computing, and human-computer interaction studies. :cite:p:`Epp2011-rj,Khanna2010-gn, Vizer2009-sg, Khan2008-is, Nahin2014-yj, Dijkstra_2013` 

There is not much research on the use of keystroke dynamics and behavioral user patterns. 
In :cite:p:`Katerina2018-ch` the authors explore the use of keystroke dynamics in correlation with end-user's behavior attributes during web-based EUD activities, revealing that this metrics reflect some correlatinons with perceieved usefulness or self-efficacy.

Typing Duration
----------------
When users type on a keyboard, each keystroke involves a key press followed by a key release. The typing duration metric captures the time interval between these two events for each keystroke. This metric is useful for analyzing typing speed or patterns. :cite:p:`Khanna2010-gn, Katerina2018-ch`.
The function :py:func:`~pywib.typing_durations` computes the typing durations from a DataFrame containing keyboard interaction data. The DataFrame should include columns for event type (key press or key release), timestamps, and keys (session or user identifiers).

Tpying Speed
-------------
This metric refers to the average number of characters typed per minute (CPM) by a user during a typing session. It provides insights into the user's typing proficiency, ease of use or emotional state :cite:p:`Khanna2010-gn, Katerina2018-ch`.
The function :py:func:`~pywib.typing_speed` calculates the average typing speed from a DataFrame containing keyboard interaction data. The DataFrame should include columns for event type (key press or key release), timestamps, and keys (session or user identifiers).
With the function :py:func:`~pywib.typing_speed_metrics` the metrics returned include: average CPM, total characters typed, and total time spent typing.

Backspace Usage 
----------------
The number of times a user presses the backspace key during a typing session can be a helpful metric to assess a negative emotional state and error correction behavior :cite:p:`Khanna2010-gn`.
The function :py:func:`~pywib.backspace_usage` computes the backspace usage from a DataFrame containing keyboard interaction data. The DataFrame should include columns for event type (key press or key release), timestamps, and keys (session or user identifiers).

.. To be added: dwell time, flight time and down-to-down time :cite:p:`Katerina2018-ch`.

References
----------
.. bibliography::
   :style: apa