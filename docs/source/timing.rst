Timing Metrics
=================

.. currentmodule:: pywib

Execution Time
--------------
Function :py:func:`~pywib.execution_time` computes the total execution time for each session by calculating the difference between the maximum and minimum timestamps within that session.

This metric provides insights into the duration of user interactions during a session, but does not account for periods of inactivity or pauses within the session.

Movement Time
--------------
Function :py:func:`~pywib.movement_time` calculates the total movement time for each session by summing the time intervals between consecutive interaction points where movement occurs.
This metric focuses on the active movement periods during a session, excluding any idle times, and provides a more accurate representation of the time spent in motion.