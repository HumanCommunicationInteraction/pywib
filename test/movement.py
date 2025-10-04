import unittest
import pandas as pd
import numpy as np

# Now you can import directly since the package is installed
from pywib.core.movement import velocity
from pywib.utils.utils import compute_space_time_diff
from utils import process_csv

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
        
        # Rest of your test code...

if __name__ == '__main__':
    unittest.main()