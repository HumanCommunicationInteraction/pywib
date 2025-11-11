Acceleration
============

.. autofunction:: pywib.acceleration

Practical Example
-----------------
.. code-block:: python

    from pywib import acceleration, velocity, compute_space_time_diff
    df = compute_space_time_diff(df_data)
    acceleration_traces = acceleration(None, velocity(df, per_traces=True), per_traces=True)
    for _, traces in acceleration_traces.items():
        for trace in traces:
            print(trace['acceleration'])

Acceleration Metrics
====================

.. autofunction:: pywib.acceleration_metrics

Practical Example
-----------------
.. code-block:: python
    
    from pywib import acceleration_metrics
    acc_metrics = acceleration_metrics(data_df)

    for _, session in acc_metrics.items():
        print(f"Session Acceleration Metrics:")
        print(f" Mean Acceleration: {session['mean']}")
        print(f" Max Acceleration: {session['max']}")
        print(f" Min Acceleration: {session['min']}")