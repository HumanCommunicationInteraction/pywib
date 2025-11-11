Jerkiness
=========
.. autofunction:: pywib.jerkiness

Practical Example
--------------------
.. code-block:: python

    from pywib import jerkiness
    jk_df = jerkiness(data_df, per_traces=True)

    for _, traces in jk_df.items():
        for trace in traces:
            print(trace[['time', 'x', 'y', 'jerkiness']].head())
   


Jerkiness Metrics
=================
.. autofunction:: pywib.jerkiness_metrics

Practical Example
--------------------
.. code-block:: python
    
    from pywib import jerkiness_metrics
    metrics = jerkiness_metrics(data_df)

    for session, session in metrics.items():
        print(f"Session: {session}, Mean Jerkiness: {session['mean']}, Max Jerkiness: {session['max']}, Min Jerkiness: {session['min']}")