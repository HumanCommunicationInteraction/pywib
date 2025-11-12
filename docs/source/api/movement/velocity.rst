Velocity
========
.. autofunction:: pywib.velocity

Practical Example
-----------------
.. code-block:: python

   from pywib import velocity

    df = compute_space_time_diff(data_frame)
    # Calculate velocity
    df_velocity = velocity(df, per_traces=True)
    
    # Iterate over traces to obtain velocity values
    for session_id, traces in df_velocity.items():
        print(f"Session ID: {session_id}")
        for trace in traces:
            print(f"Velocity values:\n{trace['velocity']}")
                

.. autofunction:: pywib.velocity_metrics

Velocity Metrics
================

Practical Example
-----------------
.. code-block:: python

   from pywib import velocity_metrics

    metrics = velocity_metrics(data_frame)

    for _, session_id in metrics.items():
        print(f"Mean Velocity: {session_id['mean']}")
        print(f"Max Velocity: {session_id['max']}")
        print(f"Min Velocity: {session_id['min']}")