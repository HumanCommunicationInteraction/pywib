import unittest
import numpy as np
from utils import process_csv, import_pyModule
import_pyModule()

from pywib import velocity, acceleration, compute_space_time_diff

class TestMovement(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create sample test data instead of relying on external CSV
        self.test_data = process_csv('E:\\Documents\\Guille\\Uni\\2025\\HCI-Web-Interaction-Analyzer\\test_window_resize_error.csv')
        
    def test_velocity(self):
        """Test velocity calculation"""
        # Compute space-time differences
        df = compute_space_time_diff(self.test_data.copy())
        
        # Calculate velocity
        df_velocity = velocity(df)
        
        # Check if the velocity column is added
        for session_id, traces in df_velocity.items():
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
                    
    def test_acceleration(self):
        """Test acceleration calculation"""
        df = compute_space_time_diff(self.test_data.copy())
        traces_velocity = velocity(df)
        
        # Calculate acceleration
        df_acceleration = acceleration(None, traces_velocity)
        
        # Check if the acceleration column is added
        for session_id, traces in df_acceleration.items():
            for trace in traces:
                self.assertIn('acceleration', trace.columns)
                # Verify acceleration calculation
                dt = trace.timeStamp.diff()
                dv = trace['velocity'].diff()
                expected_acceleration = dv / dt
                expected_acceleration.fillna(0, inplace=True)
                np.testing.assert_allclose(trace['acceleration'], expected_acceleration, rtol=1e-5, atol=1e-8)

if __name__ == '__main__':
    unittest.main()