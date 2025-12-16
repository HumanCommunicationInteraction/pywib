Keystorke Dynamics
==================

.. TODO add durations

Typing Speed
-------------

.. autofunction:: pywib.typing_speed
Practical Example
~~~~~~~~~~~~~~~~~
.. code-block:: python

   from pywib import typing_speed

    speed = typing_speed(data_frame)

    for session_id, speed_value in speed.items():
        print(f"Session ID: {session_id}")
        print(f"Typing Speed (CPM): {speed_value}")


Backspace Usage
-----------------
.. autofunction:: pywib.backspace_usage

Practical Example
~~~~~~~~~~~~~~~~~

.. code-block:: python
    
    from pywib import backspace_usage
    
     backspace_counts = backspace_usage(data_frame)
    
     for session_id, count in backspace_counts.items():
          print(f"Session ID: {session_id}")
          print(f"Backspace Usage: {count}")