import unittest
import sys
import os

import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from test.utils import assert_between_zero_inf, process_csv, import_pyModule
from balabit_dataset.data_loader import load_all_sessions

import_pyModule()
from pywib import (extract_traces_by_session, velocity, acceleration, jerkiness, compute_space_time_diff)

# Cambiar a True solo al probar en desarrollo
DEBUG = True

class TestData:

    if(DEBUG):
        trainFiles = 'test/balabit_dataset/train/test_output.csv'
        trainFeatures = 'test/balabit_dataset/train/balabit_features_training.csv'
    else:
        dataFile = 'pywib/test/balabit_dataset/train/test_output.csv'
        trainFeatures = 'pywib/test/balabit_dataset/train/balabit_features_training.csv'

"""
Test suite to verify against: https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/iet-bmt.2018.5126
https://www.ms.sapientia.ro/~manyi/mousedynamics/
"""
class TestBalabit(unittest.TestCase):
    
    def setUp(self):
        # Load the dataset
        self.df = process_csv(TestData.trainFiles)
        self.features = pd.read_csv(TestData.trainFeatures, encoding='utf-8', sep=',')

        # Extract traces by session for later use
        self.traces = extract_traces_by_session(self.df)

    def test_velocity(self):
        traces = {'0205904470': self.traces.get('session_0205904470', [])}
        vel = velocity(None, traces, per_traces=True)
        for session_id, traces in vel.items():
            for i in range (len(traces)):
                trace = traces[i]
                compare_to = self.features[self.features['session'] == int(session_id)].iloc[i]
                # Assert that velocity values are between 0 and infinity in the vel dataframe column velocity
                self.assertIn("velocity", trace.columns)
                valid_velocity = trace[np.isfinite(trace["velocity"])].copy()
                self.assertGreaterEqual(valid_velocity["velocity"].min(), 0)
                self.assertLessEqual(valid_velocity["velocity"].max(), np.inf)

                self.assertAlmostEqual(trace["velocity"].mean(), compare_to['mean_v'], delta=0.1)
                self.assertAlmostEqual(trace["velocity"].max(), compare_to['max_v'], delta=0.1)
                self.assertAlmostEqual(trace["velocity"].min(), compare_to['min_v'], delta=0.1)

if __name__ == '__main__':
    unittest.main()