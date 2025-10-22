# pywib

Pywib (Python Web Interaction Behaviour) is a library desgined for analysing and obtaning metrics from users interaction with web pages.

## How to
```python
from pywib import velocity, velocity_metrics

v = velocity(df_all_sessions)
v_metrics = velocity_metrics(None, v)
```