import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import process_csv, import_pyModule

import_pyModule()
from pywib import (velocity, acceleration, compute_space_time_diff, 
                   auc_ratio_metrics, auc_ratio, velocity_metrics, acceleration_metrics,
                   jerkiness, jerkiness_metrics)

DEBUG = True

class TestMovement(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create sample test data instead of relying on external CSV
        if(DEBUG):
            self.test_data = process_csv('pywib/test/test_data/test_window_resize_error.csv')
            self.test_data_auc = process_csv('pywib/test/test_data/test_auc.csv')
        else:
            self.test_data = process_csv('test/test_data/test_window_resize_error.csv')
            self.test_data_auc = process_csv('test/test_data/test_auc.csv')
        
    def test_velocity(self):
        """Test velocity calculation"""
        # Compute space-time differences
        df = compute_space_time_diff(self.test_data.copy())
        
        # Calculate velocity
        df_velocity = velocity(df, per_traces=True)
        
        # Check if the velocity column is added
        for _, traces in df_velocity.items():
            for trace in traces:
                self.assertIn('velocity', trace.columns)
                # Check if velocity values are non-negative
                self.assertTrue((trace['velocity'] >= 0).all())
                self.assertGreaterEqual(trace['velocity'].mean(), 0)
                # Verify velocity calculation
                dt = trace.timeStamp.diff()
                dx = trace.x.diff()
                dy = trace.y.diff()
                expected_velocity = np.sqrt(dx**2 + dy**2) / dt
                expected_velocity.fillna(0, inplace=True)
                np.testing.assert_allclose(trace['velocity'], expected_velocity, rtol=1e-5, atol=1e-8)

    def test_velocity_metrics(self):
        """Test velocity metrics calculation"""
        metrics = velocity_metrics(self.test_data.copy())

        for _, session_id in metrics.items():
            self.assertIn('mean', session_id)
            self.assertIn('max', session_id)
            self.assertIn('min', session_id)
            self.assertGreaterEqual(session_id['mean'], 0)
            self.assertGreaterEqual(session_id['max'], 0)
            self.assertGreaterEqual(session_id['min'], 0)

    def test_acceleration(self):
        """Test acceleration calculation"""
        df = compute_space_time_diff(self.test_data.copy())
        
        # Calculate acceleration
        df_acceleration = acceleration(df, per_traces=True)
        
        # Check if the acceleration column is added
        for _, traces in df_acceleration.items():
            for trace in traces:
                self.assertIn('acceleration', trace.columns)
                # Verify acceleration calculation
                dt = trace.timeStamp.diff()
                dv = trace['velocity'].diff()
                expected_acceleration = dv / dt
                expected_acceleration.fillna(0, inplace=True)
                np.testing.assert_allclose(trace['acceleration'], expected_acceleration, rtol=1e-5, atol=1e-8)

    def test_acceleration_from_traces(self):
        df = compute_space_time_diff(self.test_data.copy())
        acceleration_traces = acceleration(None, velocity(df, per_traces=True), per_traces=True)
        for _, traces in acceleration_traces.items():
            for trace in traces:
                self.assertIn('acceleration', trace.columns)
                # Verify acceleration calculation
                dt = trace.timeStamp.diff()
                dv = trace['velocity'].diff()
                expected_acceleration = dv / dt
                expected_acceleration.fillna(0, inplace=True)
                np.testing.assert_allclose(trace['acceleration'], expected_acceleration, rtol=1e-5, atol=1e-8)

    def test_acceleration_metrics(self):
        """Test acceleration metrics calculation"""
        acc_metrics = acceleration_metrics(self.test_data.copy())

        for _, session in acc_metrics.items():
            self.assertIn('mean', session)
            self.assertIn('max', session)
            self.assertIn('min', session)
            self.assertGreaterEqual(session['mean'], 0)
            self.assertGreaterEqual(session['max'], session['min'])

    def test_jerkiness(self):
        """Test jerkiness calculation"""
        jk_df = jerkiness(self.test_data.copy(), per_traces=True)

        for _, traces in jk_df.items():
            for trace in traces:
                self.assertIn('jerkiness', trace.columns)
                # Verify jerkiness calculation
                dt = trace.timeStamp.diff()
                da = trace['acceleration'].diff()
                expected_jerkiness = da / dt
                expected_jerkiness.fillna(0, inplace=True)
                np.testing.assert_allclose(trace['jerkiness'], expected_jerkiness, rtol=1e-5, atol=1e-8)

    def test_jerkiness_metrics(self):
        metrics = jerkiness_metrics(self.test_data.copy())

        for _, session in metrics.items():
            self.assertIn('mean', session)
            self.assertIn('max', session)
            self.assertIn('min', session)
            self.assertGreaterEqual(session['mean'], 0)
            self.assertGreaterEqual(session['max'], session['min'])

    def test_auc(self):
        auc = auc_ratio(self.test_data_auc.copy())
        for _, session in auc.items():
            for trace in session:
                self.assertIn('auc_ratio', trace)
                self.assertIn('auc', trace)
                self.assertGreaterEqual(trace['auc_ratio'], 0)
        
    def test_auc_metrics(self):
        auc_metrics = auc_ratio_metrics(self.test_data_auc.copy())
        for _, session in auc_metrics.items():
            self.assertIn('mean_ratio', session)
            self.assertIn('min_ratio', session)
            self.assertIn('max_ratio', session)
            self.assertGreaterEqual(session['mean_ratio'], 0)

if __name__ == '__main__':
    unittest.main()