import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import assert_between_zero_inf, process_csv, import_pyModule

import_pyModule()
from pywib import (velocity, acceleration, compute_space_time_diff, 
                   velocity_metrics, acceleration_metrics,
                   jerkiness, jerkiness_metrics)

# Cambiar a True solo al probar en desarrollo
DEBUG = True

class TestMovement(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create sample test data instead of relying on external CSV
        if(DEBUG):
            self.test_data = process_csv('test/test_data/test_window_resize_error.csv')
            self.test_data_auc = process_csv('test/test_data/test_auc.csv')
        else:
            self.test_pause = process_csv('pywib/test/test_data/pauses.csv')
            self.test_data = process_csv('pywib/test/test_data/test_window_resize_error.csv')
            self.test_data_auc = process_csv('pywib/test/test_data/test_auc.csv')
        
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
            assert_between_zero_inf(self, session_id, 'mean')
            assert_between_zero_inf(self, session_id, 'max')
            assert_between_zero_inf(self, session_id, 'min')

    def test_velocity_metrics_from_velocity_df(self):
        """Test velocity metrics from a previosly computed velocity dataframe"""
        # Compute space-time differences
        df = compute_space_time_diff(self.test_data.copy())
        
        # Calculate velocity
        df_velocity = velocity(df)
        metrics = velocity_metrics(df_velocity)

        for _, session_id in metrics.items():
            assert_between_zero_inf(self, session_id, 'mean')
            assert_between_zero_inf(self, session_id, 'max')
            assert_between_zero_inf(self, session_id, 'min')

    def test_velocity_metrics_from_velocity_traces(self):
        """Test velocity metrics from a previosly computed velocity dataframe"""
        # Compute space-time differences
        df = compute_space_time_diff(self.test_data.copy())
        
        # Calculate velocity
        df_velocity = velocity(df, per_traces=True)
        metrics = velocity_metrics(None, traces=df_velocity)

        for _, session_id in metrics.items():
            assert_between_zero_inf(self, session_id, 'mean')
            assert_between_zero_inf(self, session_id, 'max')
            assert_between_zero_inf(self, session_id, 'min')

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

    def test_acceleration_metrics_from_aceleration_df(self):
        """Test acceleration metrics from precomputed acceleration df"""
        df = compute_space_time_diff(self.test_data.copy())
        
        # Calculate acceleration
        df_acceleration = acceleration(df)
        acc_metrics = acceleration_metrics(df_acceleration)

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

    def test_jerkiness_from_df(self):
        jk_df = jerkiness(self.test_data.copy())
        metrics = jerkiness_metrics(jk_df)

        for _, session in metrics.items():
            self.assertIn('mean', session)
            self.assertIn('max', session)
            self.assertIn('min', session)
            self.assertGreaterEqual(session['mean'], 0)
            self.assertGreaterEqual(session['max'], session['min'])



if __name__ == '__main__':
    unittest.main()